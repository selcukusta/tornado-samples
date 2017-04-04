''' Handlers.py '''
import os
import uuid

import tornado.web


class MainHandler(tornado.web.RequestHandler):
    ''' Route\'ta tanimli istek url\'ini karsilayacak nesne '''

    def get(self):
        if len(self.get_query_arguments('param')) > 0:
            self.write(self.get_query_arguments('param')[0])

        # Asagidaki kullanim ile belirtilen parametre yoksa default bir deger
        # atanmasi saglanabilir...
        self.write(self.get_query_argument('param', 'NONE'))

    def data_received(self, data):
        pass


class FormHandler(tornado.web.RequestHandler):
    ''' Route\'ta tanimli istek url\'ini karsilayacak nesne '''

    def get(self):
        self.write('''<html>
            <body>
                <form action="/myform" method="POST">
                    <input type="text" name="message">
                    <input type="submit" value="Submit">
                </form>
            </body>
        </html>''')

    def post(self):
        self.write('You have entered:' +
                   self.get_body_argument('message', 'NONE'))

    def data_received(self, data):
        pass


class FileFormHandler(tornado.web.RequestHandler):
    ''' Route\'ta tanimli istek url\'ini karsilayacak nesne '''

    def get(self):
        self.write('''<html>
            <body>
                <form action="/fileform" method="POST" enctype="multipart/form-data">
                    <label for="image_name">Please give any name to image:</label>
                    <input type="text" name="image_name">
                    <br />
                    <label for="image">Please select any image to upload:</label>
                    <input type="file" name="image">
                    <br />
                    <input type="submit" value="Submit">
                </form>
            </body>
        </html>''')

    def post(self):
        if len(self.request.files) > 0 and self.request.files['image'] is not None:
            file_name = self.get_body_argument('image_name', '')
            if len(file_name) <= 0:
                file_name = str(uuid.uuid1())

            upload_path = "uploads/"
            file_info = self.request.files['image'][0]
            file_extension = os.path.splitext(file_info['filename'])[1]
            file_name = file_name + file_extension
            file_uploader = open(upload_path + file_name, 'wb')
            file_uploader.write(file_info['body'])
            self.write("{} is uploaded. Check {} folder".format(
                file_name, upload_path))
            self.finish()

        else:
            self.write(
                '<span style="color:maroon">File is not selected!</span>')

    def data_received(self, data):
        pass
