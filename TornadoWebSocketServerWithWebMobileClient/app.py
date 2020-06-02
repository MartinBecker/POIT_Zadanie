import os
import os.path
# SERVER RUNNING ON WINDOWS: import asyncio

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket

from tornado.options import parse_command_line
from tornado.escape import json_decode, json_encode
from tornado.iostream import PipeIOStream

#
# RENDER SENSORS WEB APP
#
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class TestHandler(tornado.web.RequestHandler):
    def post(self):
        print self.request.body
        self.write("ok")
        fuj = self.request.body
        fo = open("HodnotyRotacie.txt","a+")    
        fo.write("%s\r\n" %fuj)
        


#
# WEBSOCKET COMMUNICATION
#
class DataHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        print(message)

    def on_close(self):
        print("WebSocket closed")


#
# PYTHON APP INITIALISATION
#
def main():
    # SERVER RUNNING ON WINDOWS: asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    parse_command_line()

    settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"), static_path=os.path.join(os.path.dirname(__file__), "static"))
    handlers = [(r"/", MainHandler), (r"/stream", DataHandler),(r"/test", TestHandler)] 
    
    app = tornado.web.Application(handlers, **settings)

    # TODO: Change <YOUR_CERT_NAME> and <YOUR_KEY_NAME>
    http_server = tornado.httpserver.HTTPServer(app, ssl_options={"certfile": os.path.join(os.path.dirname(__file__), "cert.pem"), "keyfile": os.path.join(os.path.dirname(__file__), "key.pem")})
    http_server.listen(8080)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()