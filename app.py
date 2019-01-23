import tornado.ioloop
import tornado.web
import tornado.httpserver   #单线程的HTTP服务
import tornado.options  # 命令行解析模块，让模块定义自己的选项
from tornado.options import define, options

from handlers import main, auth

define('port', default='8000', help='listening port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/', main.IndexHandler),
            ('/explore', main.ExploreHandler),
            ('/upload', main.UploadHandler),
            ('/login', auth.LoginHandler),
            ('/post/(?P<post_id>[0-9]+)', main.PostHandler),
        ]

        settings = dict(
            debug = True,
            template_path = 'templates',
            static_path = 'static',
            cookie_secret='zhujiafu',
            login_url='/login',
            xsrf_cookies=True,
            pycket={
                'engine': 'redis',  # 设置存储器类型
                'storage': {
                    'host': '127.0.0.1',
                    'port': 6379,
                    'password': '',
                    'db_sessions': 5,
                    'db_notifications': 11,
                    'max_connections': 2 ** 31,
                },
                'cookies': {
                    'expires_days': 30,  # 设置过期时间
                },
            },
        )

        super().__init__(handlers, **settings)


application = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(options.port)
    print("Server start on port {}".format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()
