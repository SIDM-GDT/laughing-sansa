import requests
import unittest

protocol = "http"
host = "tactile-petal-92303.appspot.com"

def getUrl(URI):
    return "%s://%s/%s" %(protocol, host, URI)
 
class CreateUserTest(unittest.TestCase):
    """Create User test case"""
     
    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        requests.delete(getUrl("user/"))
        self.r = requests.get(getUrl("user/create"))
     
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
            r = requests.get(getUrl("user/create"))
            self.assertTrue(r.text not in IDs, "There is a repeat user ID")
            IDs.add(r.text)


class UserNameTest(unittest.TestCase):
    """Get User Name case"""
     
    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        requests.delete(getUrl("user"))
        r = requests.get(getUrl("user/create"))
        self.userID = r.text
        self.r = requests.get(getUrl("user/XP/%s" % self.userID))
     
    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""
        
     
    # test existing
    def testExistingID(self):
        """Test Existing ID"""
        self.assertEqual(len(self.r.text), 5, "User ID should be length 5")

    def testNonExistingID(self):
        pass

    def testBeforeSetName(self):
        pass

    def testAfterSetName(self):
        pass

    def testSetEmptyName(self):
        pass

    def testNameWithSpace(self):
        pass

    def testResetName(self):
        """ Test if the name can be set a 2nd time """
        pass

    def testInvalidName(self):
        pass
     



if __name__ == "__main__":
    unittest.main()

    # creating a new test suite
    assignment1Suite = unittest.TestSuite()
 
    # adding a test case
    assignment1Suite.addTest(unittest.makeSuite(GetUserTest))
    assignment1Suite.addTest(unittest.makeSuite(GetNameTest))


    #assignment1Runner = unittest.TextTestRunner(description=False)
    assignment1Runner = unittest.TextTestRunner()
    assignment1Runner.run(assignment1Suite)



