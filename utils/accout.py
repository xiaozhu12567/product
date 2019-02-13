import hashlib
from models.accout import User, Post, session, Like


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

def add_post_for(username, image_url, thumb_url):
    """
    保存用户上传的图片信息
    :param username:
    :param image_url:
    :param thumb_url:
    :return:
    """
    user = session.query(User).filter_by(name=username).first()
    post = Post(img_url=image_url, thumb_url=thumb_url, user=user)
    session.add(post)
    session.commit()
    return post

def get_post_for(username):
    """
    获取用户上传的图片
    :param username:
    :return:
    """
    user = session.query(User).filter_by(name=username).first()
    if user:
        return user.posts
    else:
        return []

def get_post(post_id):
    """
    获取指定id的post对象
    :param post_id:
    :return:
    """
    post = session.query(Post).filter_by(id=post_id).scalar()
    return post

def get_all_posts():
    posts = session.query(Post).order_by(Post.id.desc()).all()  # 以id降序排列
    return posts

def get_user(username):
    user = session.query(User).filter_by(name=username).first()
    return user

def get_like_posts(user):
    if user:
        posts = session.query(Post).filter(Like.user_id == user.id,
                                       Post.id == Like.post_id,
                                       Post.user_id != user.id).all()
    else:
        posts = []
    return posts

def get_like_count(post):
    count = session.query(Like).filter_by(post_id=post.id).count()
    return count