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
define("cookie_name", default="tornado-fb-user", type=str)
define("cookie_secret", default=(base64.b64encode(
    uuid.uuid4().bytes + uuid.uuid4().bytes)), type=str)
define("login_name", default="/auth/login", type=str)
define("facebook_api_key", default="<FACEBOOK API KEY>",
       help="your Facebook application API key", type=str)
define("facebook_api_secret", default="<FACEBOOK APP SECRET>",
       help="your Facebook application secret", type=str)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [(r"/", MainHandler),
                    (r"/hello-world", HelloWorldHandler),
                    (r"/auth/login", AuthLoginHandler),
                    (r"/auth/logout", AuthLogoutHandler)]

        settings = dict(cookie_secret=options.cookie_secret,
                        login_url=options.login_name,
                        template_path=os.path.join(
                            os.path.dirname(__file__), "templates"),
                        static_path=os.path.join(
                            os.path.dirname(__file__), "static"),
                        xsrf_cookies=True,
                        facebook_api_key=options.facebook_api_key,
                        facebook_secret=options.facebook_api_secret,
                        ui_modules={"Post": PostModule},
                        debug=True,
                        autoescape=None)

        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie(options.cookie_name)
        if not user_json:
            return None
        return tornado.escape.json_decode(user_json)

class MainHandler(BaseHandler, tornado.auth.FacebookGraphMixin):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("logout", "0") == "1":
            self.render("visitor.html")
            return

        current_user = self.get_current_user()
        on_receive_response = yield self.facebook_request("/me/feed", access_token=current_user["access_token"])

        if on_receive_response is None:
            self.redirect("/auth/login")
            return

        self.render("logged-in.html", stream=on_receive_response)

class HelloWorldHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write("Hello World!")

class AuthLoginHandler(BaseHandler, tornado.auth.FacebookGraphMixin):

    @tornado.gen.coroutine
    def get(self):
        url_next_part = tornado.escape.url_escape(
            self.get_argument("next", "/"))
        my_url = "{}://{}/auth/login?next={}".format(
            self.request.protocol, self.request.host, url_next_part)
        if self.get_argument("code", False):
            on_auth = yield self.get_authenticated_user(redirect_uri=my_url,
                                                        client_id=options.facebook_api_key,
                                                        client_secret=options.facebook_api_secret,
                                                        code=self.get_argument("code"))

            if not on_auth:
                raise tornado.web.HTTPError(500, "Facebook auth failed")

            self.set_secure_cookie(options.cookie_name,
                                   tornado.escape.json_encode(on_auth))
            self.redirect(self.get_argument("next", "/"))
        else:
            self.authorize_redirect(redirect_uri=my_url, client_id=options.facebook_api_key, extra_params={
                                    "scope": "user_posts"})

class AuthLogoutHandler(BaseHandler, tornado.auth.FacebookGraphMixin):

    def get(self):
        self.clear_cookie(options.cookie_name)
        self.redirect("/?logout=1")

class PostModule(tornado.web.UIModule):

    def render(self, post):
        return self.render_string("modules/feed-item.html", post=post)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()