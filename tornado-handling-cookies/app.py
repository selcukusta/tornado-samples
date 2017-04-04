''' Module aciklama alani '''
import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.web
import time


class MainHandler(tornado.web.RequestHandler):
    ''' Route\'ta tanimli istek url\'ini karsilayacak nesne '''

    def get(self):
        if self.get_cookie('Hello') is None:
            expires = time.time() + 7 * 24 * 3600
            expire_date = str(time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(expires)))
            self.add_header(
                "Set-Cookie", "Hello=World; expires={0}; path=/".format(expire_date))
            self.write("Cookie is added!")
        else:
            self.write("Cookie value is: " + self.get_cookie('Hello'))
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
