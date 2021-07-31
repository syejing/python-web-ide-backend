import time

import tornado.web
from tornado.web import RequestHandler


class HomeHandler(RequestHandler):
    def get_current_user(self):
        token = self.get_secure_cookie("token", None)
        if token is None:
            return False
        return True

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render("home.html", now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


class StaticFileHandler(tornado.web.StaticFileHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.xsrf_token)
