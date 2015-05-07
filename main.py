import webapp2


class DefaultHandler(webapp2.RequestHandler):
    def respond(self, httpVerb, URI=None):
        self.response.write('HTTP verb is %s<br>' % httpVerb)
        self.response.write('HTTP URI is %s<br>' % URI)

    def get(self, URI):        
        self.respond('GET', URI)

    def post(self, URI):        
        self.respond('POST', URI)

    def put(self, URI):        
        self.respond('PUT', URI)

    def delete(self, URI):
        self.respond('DELETE', URI)



routes = [
    (r'/(.*)', DefaultHandler),
]

config = {}


app = webapp2.WSGIApplication(routes=routes, debug=True, config=config)

def main():
    app.run()

if __name__ == '__main__':
    main()

