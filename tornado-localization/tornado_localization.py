#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import base64
import uuid

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("locale_path", default=os.path.join(os.path.dirname(__file__), "locales"), type=str)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [(r"/", MainHandler)]

        settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"),
                        debug=True,
                        autoescape=None)

        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    def get_user_locale(self):
        code = self.get_argument("code", "tr")
        if code == "en":
            return tornado.locale.get("en_EN")
        elif code == "de":
            return tornado.locale.get("de_DE")
        else:
            return tornado.locale.get("tr_TR")

class MainHandler(BaseHandler):
    def get(self):
        self.render("default.html")

def main():
    tornado.options.parse_command_line()
    tornado.locale.load_translations(options.locale_path, "windows-1254")
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
