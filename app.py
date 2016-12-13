import tornado.ioloop
import tornado.web

from api.routes import routes
from api.settings import settings


def make_app():
    return tornado.web.Application(routes, **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
