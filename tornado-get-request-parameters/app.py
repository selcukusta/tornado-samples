''' Module aciklama alani '''
import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.web

import handlers


class Application(tornado.web.Application):
    ''' Uygulama ana sinifi '''

    def __init__(self):
        _handlers = [
            (r'/', handlers.MainHandler),
            (r'/myform', handlers.FormHandler),
            (r'/fileform', handlers.FileFormHandler)
        ]
        tornado.web.Application.__init__(self, _handlers)

if __name__ == "__main__":

    HTTP_SERVER = tornado.httpserver.HTTPServer(Application())
    HTTP_SERVER.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
