""" Define Handlers """
import json
import tornado.web
import helpers

class MainHandler(tornado.web.RequestHandler):
    """ Is API working properly """

    async def get(self):
        self.write("call /api/viewcount/{news-id}")

    def data_received(self, data):
        pass


class PageViewCount(tornado.web.RequestHandler):
    """ Get page view count from Redis"""

    async def get(self, content_id):
        """ GET request """
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET")
        self.set_header('Content-Type', 'application/json')

        if content_id:
            count = await helpers.get_count(content_id)
            self.write(json.dumps({"count": count}))
        else:
            self.write(json.dumps({"count": "ERROR"}))

    def data_received(self, data):
        pass
