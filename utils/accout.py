import hashlib


def hashed(text):
    return hashlib.md5(text.encode('utf8')).hexdigest()


USER_DATA = {
    "name": "zhujiafu",
    "password": hashed("123.coM")
}


def authenticate(username, password):
    """
    校验用户名和密码是否符合记录
    :param username:
    :param password:
    :return: True代表通过验证
    """
    if username and password:
        return username == USER_DATA['name'] and hashed(password) == USER_DATA['password']
    else:
        return False