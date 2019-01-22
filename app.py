import tornado.ioloop
import tornado.web
import tornado.httpserver   #单线程的HTTP服务
import tornado.options  # 命令行解析模块，让模块定义自己的选项
from tornado.options import define, options

from handlers import main

define('port', default='8000', help='listening port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/', main.IndexHandler),
            ('/explore', main.ExploreHandler),
            ('/post/(?P<post_id>[0-9]+)', main.PostHandler),
        ]

        settings = dict(
            debug = True,
            template_path = 'templates',
            static_path = 'static',
        )

        super().__init__(handlers, **settings)


application = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(options.port)
    print("Server start on port {}".format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()
