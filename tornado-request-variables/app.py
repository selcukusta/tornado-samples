''' Module aciklama alani '''
import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    ''' Route\'ta tanimli istek url\'ini karsilayacak nesne '''

    def get(self):
        self.write("<h2>Request Variables</h2>")

        self.write("<strong>Method</strong>: " +
                   self.request.method + "<br />")

        self.write("<strong>Uri</strong>: " + self.request.uri + "<br />")

        self.write("<strong>Path</strong>: " + self.request.path + "<br />")

        self.write("<strong>Query</strong>: " + self.request.query + "<br />")

        self.write("<strong>Full URL</strong>: " +
                   self.request.full_url() + "<br />")

        self.write("<strong>HTTP Version</strong>: " +
                   self.request.version + "<br />")

        self.write("<strong>Request Time</strong>: " +
                   str(self.request.request_time()) + "<br />")

        self.write("<h2>Request Header Variables</h2>")

        for header in self.request.headers:
            self.write("<strong>" + header + "</strong>" + ": " +
                       self.request.headers[header] + " <br />")

        self.write("<hr />")

        self.write('''
        For more attributes:
        <a href="http://www.tornadoweb.org/en/stable/httputil.html#tornado.httputil.HTTPServerRequest" target="_blank">
            Tornado Documentation
        </a>''')

    def data_received(self, data):
        pass


class Application(tornado.web.Application):
    ''' Uygulama ana sinifi '''

    def __init__(self):
        _handlers = [
            (r'/', MainHandler)
        ]
        tornado.web.Application.__init__(self, _handlers)

if __name__ == "__main__":

    HTTP_SERVER = tornado.httpserver.HTTPServer(Application())
    HTTP_SERVER.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
