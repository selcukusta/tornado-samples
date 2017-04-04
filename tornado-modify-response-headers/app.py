''' Module aciklama alani '''
import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.web
import json


class MainHandler(tornado.web.RequestHandler):
    ''' Route\'ta tanimli istek url\'ini karsilayacak nesne '''

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET")
        self.set_header('Content-Type', 'application/json')
        self.set_header("X-Forwarded-For", "ngnix")
        self.clear_header("Date")
        self.write(json.dumps(
            {
                'response':
                {
                    'statusCode': 200,
                    'statusMessage': 'Request is received successfully!'
                }
            }
        ))

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
