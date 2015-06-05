import requests
import unittest
import json

protocol = "http"
#host = "tactile-petal-92303.appspot.com"
host = "localhost:8080"

def genUrl(URI):
    return "%s://%s/%s" %(protocol, host, URI)
 
class CreateUserIDTest(unittest.TestCase):
    """Create User test case"""
     
    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        requests.delete(genUrl("user/"))
        self.r = requests.get(genUrl("user/create/"))
     
    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""
        
     
    # test length
    def testLength5(self):
        """Test length 5"""
        self.assertEqual(len(self.r.text), 5, "User ID should be length 5")
     
    # test lowercase
    def testAllLower(self):
        """Test all lower"""
        lowercase_letters = ''.join(c for c in self.r.text if c.islower())
        self.assertEqual(len(lowercase_letters), 5, "All IDs should be lowercase")

    #test alphabets
    def testAllCharacters(self):
        import string
        alphabets = ''.join(c for c in self.r.text if c in string.ascii_letters)
        self.assertEqual(len(alphabets), 5, "All IDs should be alphabets")

    #test no repeat
    def testNoRepeat(self):
        IDs = set()
        IDs.add(self.r.text)
        for n in range(1):
            r = requests.get(genUrl("user/create/"))
            self.assertTrue(r.text not in IDs, "There is a repeat user ID")
            IDs.add(r.text)

class UserTest(unittest.TestCase):
    """Get User case"""
     
    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        requests.delete(genUrl("user/"))
        
     
    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""
        
     
    # test existing
    def testCreateUser(self):
        """Test Existing ID"""
        r = requests.get(genUrl("user/create/"))
        userID = r.text
        r = requests.get(genUrl("user/%s" % userID))
        self.assertEqual(r.status_code, 200, "There should be a user created")

    def testDeleteUser(self):
        r = requests.get(genUrl("user/create/"))
        userID = r.text
        r = requests.delete(genUrl("user/%s" % userID))
        self.assertEqual(r.status_code, 200, "Status code of delete user should be 200")
        r = requests.get(genUrl("user/%s" % userID))
        self.assertEqual(r.status_code, 404)

    def testGetUserInfo(self):
        """ Test if the information from server is correct"""
        r = requests.get(genUrl("user/create/"))
        userID = r.text
        r = requests.get(genUrl("user/%s" % userID))
        try:
            r.json()
        except ValueError:
            self.assertTrue(False, "No JSON object could be decoded")

    def testGetDefaultUserInfo(self):
        r = requests.get(genUrl("user/create/"))
        userID = r.text
        r = requests.get(genUrl("user/%s" % userID))
        try:
            obj = r.json()
            self.assertIn("Name", obj)
            self.assertIn("XP", obj)
            self.assertIn("Level", obj)
            self.assertIn("Gold", obj)
            self.assertEqual(obj["Name"], "")
            self.assertEqual(obj["XP"], 0)
            self.assertEqual(obj["Level"], 1)
            self.assertEqual(obj["Gold"], 0) 
        except ValueError:
            self.assertTrue(False, "No JSON object could be decoded")
        

    def testGetAlteredUserInfo(self):
        r = requests.get(genUrl("user/create/"))
        userID = r.text
        r = requests.put(genUrl("user/gold/%s"%userID), data="100")
        r = requests.put(genUrl("user/XP/%s"%userID), data="100")
        r = requests.get(genUrl("user/%s" % userID))
        try:
            obj = r.json()
            self.assertIn("Name", obj)
            self.assertIn("XP", obj)
            self.assertIn("Level", obj)
            self.assertIn("Gold", obj)
            self.assertEqual(obj["Name"], "")
            self.assertEqual(obj["XP"], 100)
            self.assertEqual(obj["Level"], 2)
            self.assertEqual(obj["Gold"], 100) 
        except ValueError:
            self.assertTrue(False, "No JSON object could be decoded")

    def testDelete1User(self):
        """ Create 2 users, delete 1, check if it is properly deleted"""
        r = requests.get(genUrl("user/create/"))
        userID1 = r.text
        r = requests.get(genUrl("user/create/"))
        userID2 = r.text
        r = requests.delete(genUrl("user/%s" % userID1))
        r = requests.get(genUrl("user/%s" % userID1))
        self.assertEqual(r.status_code, 404)
        r = requests.get(genUrl("user/%s" % userID2))
        try:
            obj = r.json()

            self.assertIn("Name", obj)
            self.assertIn("XP", obj)
            self.assertIn("Level", obj)
            self.assertIn("Gold", obj)
            self.assertEqual(obj["Name"], "")
            self.assertEqual(obj["XP"], 0)
            self.assertEqual(obj["Level"], 1)
            self.assertEqual(obj["Gold"], 0) 

        except ValueError:
            self.assertTrue(False, "No JSON object could be decoded")


    def testDeleteAllUsers(self):
        r = requests.get(genUrl("user/create/"))
        userID1 = r.text
        r = requests.get(genUrl("user/create/"))
        userID2 = r.text
        r = requests.delete(genUrl("user/"))
        self.assertEqual(r.status_code, 200, "Status code of delete all users should be 200")
        r = requests.get(genUrl("user/%s" % userID1))
        self.assertEqual(r.status_code, 404)
        r = requests.get(genUrl("user/%s" % userID2))
        self.assertEqual(r.status_code, 404)


class UserNameTest(unittest.TestCase):
    """Get User Name case"""
     
    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        requests.delete(genUrl("user/"))
        r = requests.get(genUrl("user/create/"))
        self.userID = r.text
     
    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""
        
    def getUserName(self, userID=None):
        if not userID:
            userID = self.userID
        r = requests.get(genUrl("user/%s" % userID))
        try:
            obj = r.json()
            self.assertIn("Name", obj, "There should be a key \'Name\'")
            return obj["Name"]
        except ValueError:
            self.assertTrue(False, "No JSON object could be decoded")

    # test existing
    def testExistingID(self):
        """Test Existing ID with no user name set"""
        userName = self.getUserName()
        self.assertEqual(userName, "", "Username should be blank by default")

    def testNonExistingID(self):
        userID = "aaaaa"
        r = requests.get(genUrl("user/%s" % userID))
        self.assertEqual(r.status_code, 404, "Non existing user")

    def testSetName(self):
        userName = "wangchuck"
        r = requests.post(genUrl("user/name/%s" % self.userID), data=userName)
        self.assertEqual(r.status_code, 200, "Set user name should be successful")
        self.assertEqual(self.getUserName(), userName, "User name retrieved should be the same as the one set")

    def testSetEmptyName(self):
        userName = ""
        r = requests.post(genUrl("user/name/%s" % self.userID), data=userName)
        self.assertEqual(r.status_code, 400, "User name should not be the same")
        self.assertEqual(self.getUserName(), userName, "User name retrieved should be the same as the one set")

    def testSetEmptyThenValidName(self):
        userName = ""
        r = requests.post(genUrl("user/name/%s" % self.userID), data=userName)
        self.assertEqual(r.status_code, 400, "User name should not be the same")
        self.assertEqual(self.getUserName(), userName, "User name retrieved should be the same as the one set")

        userName = "wangchuck"
        r = requests.post(genUrl("user/name/%s" % self.userID), data=userName)
        self.assertEqual(r.status_code, 200, "Set user name should be successful")
        self.assertEqual(self.getUserName(), userName, "User name retrieved should be the same as the one set")

    def testNameWithSpace(self):
        userName = "Mother of Dragons"
        r = requests.post(genUrl("user/name/%s" % self.userID), data=userName)
        self.assertEqual(r.status_code, 200, "Set user name should be successful")
        self.assertEqual(self.getUserName(), userName, "User name retrieved should be the same as the one set")

    def testResetName(self):
        """ Test if the name can be set a 2nd time """
        userName1 = "wangchuck"
        r = requests.post(genUrl("user/name/%s" % self.userID), data=userName1)
        self.assertEqual(r.status_code, 200, "Set user name should be successful")
        self.assertEqual(self.getUserName(), userName1, "User name retrieved should be the same as the one set")
        
        userName2 = "Waterloo"
        r = requests.post(genUrl("user/name/%s" % self.userID), data=userName2)
        self.assertEqual(r.status_code, 405, "Set user name should be unsuccessful 405")
        self.assertEqual(self.getUserName(), userName1, "User name retrieved should be the same as the first one set")

    def testInvalidName(self):
        userName = "@$%^"
        r = requests.post(genUrl("user/name/%s" % self.userID), data=userName)
        self.assertEqual(r.status_code, 400, "Should be a bad request, bad user name")
        self.assertEqual(self.getUserName(), "", "User name retrieved should be empty")
     
class XPTest(unittest.TestCase):
    """Get User XP case"""
     
    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        requests.delete(genUrl("user/"))
        r = requests.get(genUrl("user/create/"))
        self.userID = r.text
     
    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""
        
     
    # test existing
    def testExistingID(self):
        """Test Existing ID to see if the call passes"""
        r = requests.get(genUrl("user/XP/%s" % self.userID))
        self.assertEqual(r.status_code, 200, "Status code should be 200")

    def testNonExistingID(self):
        """ to see if the call fails """
        r = requests.get(genUrl("user/XP/%s" % "aaaaa"))
        self.assertEqual(r.status_code, 404, "Status code should be 404 not found")

        XPVal = "300"
        r = requests.put(genUrl("user/XP/%s" % "aaaaa"), data=XPVal)
        self.assertEqual(r.status_code, 404, "Status code should be 404 not found")

    def testSetValidXP(self):
        XPVal = "300"
        r = requests.put(genUrl("user/XP/%s" % self.userID), data=XPVal)
        self.assertEqual(r.status_code, 200, "Status code should be 200")

        r = requests.get(genUrl("user/XP/%s" % self.userID))
        self.assertEqual(r.text, XPVal, "XP should be set")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

    def testSetHigherXP(self):
        XPVal = "300"
        r = requests.put(genUrl("user/XP/%s" % self.userID), data=XPVal)
        self.assertEqual(r.status_code, 200, "Status code should be 200")

        r = requests.get(genUrl("user/XP/%s" % self.userID))
        self.assertEqual(r.text, XPVal, "XP should be set")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

        highXPVal = "400"
        r = requests.put(genUrl("user/XP/%s" % self.userID), data=highXPVal)
        self.assertEqual(r.status_code, 200, "Status code should be 400, XP won't go lower")

        r = requests.get(genUrl("user/XP/%s" % self.userID))
        self.assertEqual(r.text, highXPVal, "XP should be set")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

    def testSetLowerXP(self):
        XPVal = "300"
        r = requests.put(genUrl("user/XP/%s" % self.userID), data=XPVal)
        self.assertEqual(r.status_code, 200, "Status code should be 200")

        r = requests.get(genUrl("user/XP/%s" % self.userID))
        self.assertEqual(r.text, XPVal, "XP should be set")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

        lowXPVal = "200"
        r = requests.put(genUrl("user/XP/%s" % self.userID), data=lowXPVal)
        self.assertEqual(r.status_code, 400, "Status code should be 400, XP won't go lower")

        r = requests.get(genUrl("user/XP/%s" % self.userID))
        self.assertEqual(r.text, XPVal, "XP should be set")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

    def testGetDefaultXP(self):
        r = requests.get(genUrl("user/XP/%s" % self.userID))
        self.assertEqual(r.text, "0", "XP should be 0 by default")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

    def testSetNegativeXP(self):
        XPVal = "-300"
        r = requests.put(genUrl("user/XP/%s" % self.userID), data=XPVal)
        self.assertEqual(r.status_code, 400, "Status code should be 400, no negative values")

        r = requests.get(genUrl("user/XP/%s" % self.userID))
        self.assertEqual(r.text, "0", "XP should be 0 by default")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

    def testSetAlphabetXP(self):
        XPVal = "abc"
        r = requests.put(genUrl("user/XP/%s" % self.userID), data=XPVal)
        self.assertEqual(r.status_code, 400, "Status code should be 400, no alphabet values")

        r = requests.get(genUrl("user/XP/%s" % self.userID))
        self.assertEqual(r.text, "0", "XP should be 0 by default")
        self.assertEqual(r.status_code, 200, "Status code should be 200")



class GoldTest(unittest.TestCase):
    """Gold test case"""
     
    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        requests.delete(genUrl("user/"))
        r = requests.get(genUrl("user/create/"))
        self.userID = r.text
        
     
    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""
        
     
    # test existing
    def testExistingID(self):
        """Test Existing ID to see if call passes"""
        r = requests.get(genUrl("user/gold/%s" % self.userID))
        self.assertEqual(r.status_code, 200, "Status code should be 200")

    def testNonExistingID(self):
        """ Test non existing ID to see if call fails """
        r = requests.get(genUrl("user/gold/%s" % "aaaaa"))
        self.assertEqual(r.status_code, 404, "Status code should be 404 not found")

        goldVal = "300"
        r = requests.put(genUrl("user/gold/%s" % "aaaaa"), data=goldVal)
        self.assertEqual(r.status_code, 404, "Status code should be 404 not found")

    def testSetValidGold(self):
        goldVal = "300"
        r = requests.put(genUrl("user/gold/%s" % self.userID), data=goldVal)
        self.assertEqual(r.status_code, 200, "Status code should be 200")

        r = requests.get(genUrl("user/gold/%s" % self.userID))
        self.assertEqual(r.text, goldVal, "Gold value should be set")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

    def testSetMoreOrLessGold(self):
        goldVal1 = "300"
        r = requests.put(genUrl("user/gold/%s" % self.userID), data=goldVal1)
        self.assertEqual(r.status_code, 200, "Status code should be 200")

        r = requests.get(genUrl("user/gold/%s" % self.userID))
        self.assertEqual(r.text, goldVal1, "Gold value should be set")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

        goldVal2 = "400"
        r = requests.put(genUrl("user/gold/%s" % self.userID), data=goldVal2)
        self.assertEqual(r.status_code, 200, "Status code should be 200")

        r = requests.get(genUrl("user/gold/%s" % self.userID))
        self.assertEqual(r.text, goldVal2, "Gold value should be set")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

        goldVal3 = "100"
        r = requests.put(genUrl("user/gold/%s" % self.userID), data=goldVal3)
        self.assertEqual(r.status_code, 200, "Status code should be 200")

        r = requests.get(genUrl("user/gold/%s" % self.userID))
        self.assertEqual(r.text, goldVal3, "Gold value should be set")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

    def testGetDefaultGold(self):
        r = requests.get(genUrl("user/gold/%s" % self.userID))
        self.assertEqual(r.text, "0", "Gold should be 0 by default")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

    def testSetNegativeGold(self):
        goldVal = "-300"
        r = requests.put(genUrl("user/gold/%s" % self.userID), data=goldVal)
        self.assertEqual(r.status_code, 400, "Status code should be 400, no negative gold")

        r = requests.get(genUrl("user/gold/%s" % self.userID))
        self.assertEqual(r.text, "0", "Gold value should be 0 by default")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

    def testSetAlphabetGold(self):
        goldVal = "jiu"
        r = requests.put(genUrl("user/gold/%s" % self.userID), data=goldVal)
        self.assertEqual(r.status_code, 400, "Status code should be 400, no alphabet gold")

        r = requests.get(genUrl("user/gold/%s" % self.userID))
        self.assertEqual(r.text, "0", "Gold value should be 0 by default")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

class LevelTest(unittest.TestCase):
    """Get User level case"""
     
    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        requests.delete(genUrl("user/"))
        r = requests.get(genUrl("user/create/"))
        self.userID = r.text    
     
    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""
        
     
    # test existing
    def testExistingID(self):
        """Test Existing ID"""
        r = requests.get(genUrl("user/level/%s" % self.userID))
        self.assertEqual(r.status_code, 200, "Status code should be 200")

    def testNonExistingID(self):
        """ to see if the call fails """
        r = requests.get(genUrl("user/level/%s" % "aaaaa"))
        self.assertEqual(r.status_code, 404, "Status code should be 404 not found")

        XPVal = "300"
        r = requests.put(genUrl("user/level/%s" % "aaaaa"), data=XPVal)
        self.assertEqual(r.status_code, 405, "Status code should be 405 not allowed")

    def testSetValidLevel(self):
        XPVal = "300"
        r = requests.put(genUrl("user/XP/%s" % self.userID), data=XPVal)
        self.assertEqual(r.status_code, 200, "Status code should be 200")

        levelVal = "4"
        r = requests.get(genUrl("user/level/%s" % self.userID))
        self.assertEqual(r.text, levelVal, "Level should be set")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

    def testGetDefaultLevel(self):
        r = requests.get(genUrl("user/level/%s" % self.userID))
        self.assertEqual(r.text, "1", "Level should be default 1")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

    def testSetLowerLevels(self):
        """Set first time"""
        XPVal = "300"
        r = requests.put(genUrl("user/XP/%s" % self.userID), data=XPVal)
        self.assertEqual(r.status_code, 200, "Status code should be 200")

        levelVal = "4"
        r = requests.get(genUrl("user/level/%s" % self.userID))
        self.assertEqual(r.text, levelVal, "Level should be set")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

        """Set lower Level"""
        XPVal = "200"
        r = requests.put(genUrl("user/XP/%s" % self.userID), data=XPVal)
        self.assertEqual(r.status_code, 400, "Status code should be 400, level set should not be lower")

        levelVal = "4"
        r = requests.get(genUrl("user/level/%s" % self.userID))
        self.assertEqual(r.text, levelVal, "Level should be set")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

    def testSetHigherLevels(self):
        """Set first time"""
        XPVal = "300"
        r = requests.put(genUrl("user/XP/%s" % self.userID), data=XPVal)
        self.assertEqual(r.status_code, 200, "Status code should be 200")

        levelVal = "4"
        r = requests.get(genUrl("user/level/%s" % self.userID))
        self.assertEqual(r.text, levelVal, "Level should be set")
        self.assertEqual(r.status_code, 200, "Status code should be 200")

        """Set higher Level"""
        XPVal = "400"
        r = requests.put(genUrl("user/XP/%s" % self.userID), data=XPVal)
        self.assertEqual(r.status_code, 200, "Status code should be 200")

        levelVal = "5"
        r = requests.get(genUrl("user/level/%s" % self.userID))
        self.assertEqual(r.text, levelVal, "Level should be set correctly")
        self.assertEqual(r.status_code, 200, "Status code should be 200")


if __name__ == "__main__":
    unittest.main()

    # creating a new test suite
    assignment1Suite = unittest.TestSuite()
 
    # adding a test case
    
    assignment1Suite.addTest(unittest.makeSuite(GetUserTest))
    assignment1Suite.addTest(unittest.makeSuite(NameTest))
    assignment1Suite.addTest(unittest.makeSuite(GetNameTest))
    assignment1Suite.addTest(unittest.makeSuite(XPTest))
    assignment1Suite.addTest(unittest.makeSuite(GoldTest))
    assignment1Suite.addTest(unittest.makeSuite(LevelTest))
    

    #assignment1Runner = unittest.TextTestRunner(description=False)
    assignment1Runner = unittest.TextTestRunner()
    testResult = assignment1Runner.run(assignment1Suite)



