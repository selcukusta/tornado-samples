''' Module aciklama alani '''
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    ''' Route\'ta tanimli istek url\'ini karsilayacak nesne '''
    def get(self):
        self.write("Hello, world")

    def data_received(self, data):
        pass

def application_start():
    ''' Uygulamanin baslangic noktasi '''
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    APP = application_start()
    APP.listen(8888)
    tornado.ioloop.IOLoop.current().start()
