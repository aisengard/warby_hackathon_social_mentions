import routes
import tornado.httpserver
import tornado.ioloop


if __name__ == '__main__':
    application = tornado.web.Application(routes.routes())
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()