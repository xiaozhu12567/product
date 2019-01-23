import tornado.web
from utils.accout import authenticate
from pycket.session import SessionMixin


class LoginHandler(tornado.web.RequestHandler, SessionMixin):
    """
    登陆接口
    """
    def get(self, *args, **kwargs):
        next = self.get_argument('next', None)
        self.render('login.html', next=next)

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)

        if authenticate(username, password):
            self.session.set("user", username)
            next = self.get_argument('next', None)
            self.redirect(next)
        else:
            self.write("fail")
