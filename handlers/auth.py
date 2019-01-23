import tornado.web
from utils.accout import authenticate, register
from .main import AuthBaseHandler


class LoginHandler(AuthBaseHandler):
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


class LogoutHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        self.session.delete('user')


class SignupHandler(AuthBaseHandler):
    """
    注册创建用户
    """
    def get(self, *args, **kwargs):
        self.render('signup.html', msg='')

    def post(self, *args, **kwargs):
        name = self.get_argument('username', None)
        password1 = self.get_argument('password1',None)
        password2 = self.get_argument('password2',None)

        msg = ''
        if name and password1 and password2:
            if password1 == password2:
                result = register(name, password1)      # 判断用户是否存在，不存在就添加
                if result['msg'] == 'ok':
                    self.session.set('user', name)
                    self.redirect('/')
                else:
                    msg = result['msg']
            else:
                msg = 'password 不匹配'
        else:
            msg = "empty username or password"

        self.render('signup.html', msg=msg)
