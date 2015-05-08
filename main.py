import webapp2


class DefaultHandler(webapp2.RequestHandler):
    def respond(self, httpVerb, URI=None):
        self.response.write('HTTP verb is %s<br>\n' % httpVerb)
        self.response.write('HTTP URI is %s<br><br>\n' % URI)

        headers = self.request.headers
        self.response.write('List of HTTP Headers<br>\n')
        for k, v in headers.iteritems():
            self.response.write('<b>%s</b> - %s <br>\n' % (k, v))

        self.response.write('<br><b>Body of HTTP Request</b><br>\n%s'% self.request.body)

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

