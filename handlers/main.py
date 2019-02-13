import tornado.web
import glob
from utils import photo
from pycket.session import SessionMixin
from utils.accout import add_post_for, get_post_for, get_post, get_all_posts, get_user, get_like_posts, get_like_count
from utils.photo import UploadImageSave

class AuthBaseHandler(tornado.web.RequestHandler, SessionMixin):
    """
    基础的认证handler
    """
    def get_current_user(self):
        return self.session.get('user', None)


class IndexHandler(AuthBaseHandler):
    """
    首页，显示用户关注图片流
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        posts = get_post_for(self.current_user)
        self.render('index.html', posts=posts)


class ExploreHandler(AuthBaseHandler):
    """
    发现页，最近上传的图片
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        posts = get_all_posts()
        self.render('explore.html', posts=posts)


class PostHandler(AuthBaseHandler):
    """
    单个图片详情页
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        post = get_post(kwargs['post_id'])
        if post:
            like_count = get_like_count(post)
            self.render('post.html', post=post, like_count=like_count)
        else:
            self.write('post id {} is wrong'.format(kwargs['post_id']))


class UploadHandler(AuthBaseHandler):
    """
    提供表单和处理上传图片文件
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('upload.html')

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        file_list = self.request.files.get('newimg', None)
        post_id = 0
        for upload in file_list:
            name = upload['filename']
            content = upload['body']
            ims = UploadImageSave(self.settings['static_path'], name)
            ims.save_upload(content)
            ims.make_thumb()

            post = add_post_for(self.current_user, ims.image_url, ims.thumb_url)
            post_id = post.id

        self.redirect('/post/{}'.format(post_id))


class ProfileHandler(AuthBaseHandler):
    """
    用户信息页面
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        username = self.get_argument('name','')
        if not username:
            username = self.current_user
        user = get_user(username)
        like_posts = get_like_posts(user)
        self.render('profile.html', user=user, like_posts=like_posts)








