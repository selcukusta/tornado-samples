""" Main Application """
import tornado.ioloop
import tornado.autoreload
import tornado.httpserver
import handlers
from tornado.options import define, options

define("port", default=8888, help="Run on the given port", type=int)

class Application(tornado.web.Application):
    """ Main application class """
    def __init__(self):
        _handlers = [(r"/", handlers.MainHandler),
            (r"/api/viewcount/(\d*)", handlers.PageViewCount)]

        tornado.web.Application.__init__(self, _handlers)

if __name__ == "__main__":
    options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
