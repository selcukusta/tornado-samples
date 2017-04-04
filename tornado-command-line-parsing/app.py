''' Module aciklama alani '''
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import define, options

''' Global degiskenleri tanimlamak icin asagidaki kullanim uygundur '''
define("port", default=8888, help="Run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    ''' Route\'ta tanimli istek url\'ini karsilayacak nesne '''

    def get(self):
        self.write(
            "Hello, world. I'm another instance and working on: " + str(options.port))

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
    '''
    Parametreden gonderilen global degiskenlerin uygulama tarafindan yakalanabilmesi icin
    asagidaki satir mutlaka yazilmalidir
    '''
    options.parse_command_line()
    HTTP_SERVER = tornado.httpserver.HTTPServer(Application())
    HTTP_SERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
