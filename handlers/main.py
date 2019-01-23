import tornado.web
import glob
from utils import photo
from pycket.session import SessionMixin

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
        names = glob.glob('static/uploads/*.jpg')
        self.render('index.html', names=names)


class ExploreHandler(AuthBaseHandler):
    """
    发现页，最近上传的图片
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        names = glob.glob('static/uploads/thumbnail/*')
        print(names)
        self.render('explore.html', names=names)


class PostHandler(AuthBaseHandler):
    """
    单个图片详情页
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('post.html', post_id=kwargs['post_id'])


class UploadHandler(AuthBaseHandler):
    """
    提供表单和处理上传图片文件
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('upload.html')

    def post(self, *args, **kwargs):
        file_list = self.request.files.get('newimg', None)
        for upload in file_list:
            name = upload['filename']
            content = upload['body']
            photo.save_upload(name, content)
            photo.make_thumb(name, (200,200))

        self.write('upload done')







