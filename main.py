import webapp2


class DefaultHandler(webapp2.RequestHandler):
    def respond(self, httpVerb):
        self.response.write('HTTP verb is %s' % httpVerb)

    def get(self):        
        self.respond('GET')

    def post(self):        
        self.respond('POST')

    def put(self):        
        self.respond('PUT')

    def delete(self):
        self.respond('DELETE')



routes = [
    (r'/', DefaultHandler),
]

config = {}


app = webapp2.WSGIApplication(routes=routes, debug=True, config=config)

def main():
    app.run()

if __name__ == '__main__':
    main()

