import sys
import platform
import asyncio

import tornado.ioloop
import tornado.httpserver

from application import Application
import config

if sys.version_info.major >= 3 and sys.version_info.minor >= 8:
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


if __name__ == "__main__":
    try:
        app = Application()
        httpServer = tornado.httpserver.HTTPServer(app)
        httpServer.listen(config.options["port"])
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        pass
