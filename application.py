import os

import tornado.web
from tornado.web import url

from views import index, account, api, wechat
import config


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            url(r"/home", index.HomeHandler),
            url(r"/login", account.LoginHandler),
            url(r"/account/login", account.LoginHandler2),
            url(r"/logout", account.LogOutHandler),
            url(r"/api/login", api.LoginHandler),
            url(r"/wechat", wechat.WeChatHandler),
            url(r"/input", wechat.InputHandler),
            url(r"/(.*)$", index.StaticFileHandler, {"path": os.path.join(config.BASE_DIRS, "app/dist"),
                                                     "default_filename": "index.html"})
        ]
        super().__init__(handlers, **config.settings)
