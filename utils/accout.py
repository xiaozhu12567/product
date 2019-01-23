import hashlib
from models.accout import User


def hashed(text):
    return hashlib.md5(text.encode('utf8')).hexdigest()     # 密码加密


def authenticate(username, password):
    """
    校验用户名和密码是否符合记录
    :param username:
    :param password:
    :return: True代表通过验证
    """
    if username and password:
        hashed_password = User.get_password(username)
        return hashed(password) == hashed_password
    else:
        return False


def register(username, password):
    """
    注册用户，增加用户信息到数据库
    :param username:
    :param password:
    :return:
    """
    if not User.is_exists(username):
        User.add_user(username, hashed(password))
        return {"msg": "ok"}
    else:
        return {"msg": "username is exists"}