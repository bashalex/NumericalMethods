import tornado.web

from api.models import steps, params
from model.tabulation import *
from model import data
import usecases


def generate_id(_id):
    return "step{}".format(_id)


class MainHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get(self):
        self.render("main.html", steps=steps, generateId=generate_id)

    def post(self):
        action = self.get_argument('action')
        if action == 'update_function':
            name = self.get_argument('func_name')
            function = self.get_argument('func')
            save_tabulated_func(name, function)
        elif action == 'update_params':
            params.b = self.get_argument('paramB')
            # params.b1 = self.get_argument('paramB1')
            params.x = self.get_argument('paramX')
            params.y = self.get_argument('paramY')
            print(params.b, params.x, params.y)
            data.save_params(params.b, params.x, params.y, params.b1)
        elif action == 'run_tests':
            usecases.run()
