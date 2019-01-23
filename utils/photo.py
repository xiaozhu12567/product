import os
from PIL import Image

def save_upload(name, content):
    with open('static/uploads/{}'.format(name), 'wb') as f:
        f.write(content)

def make_thumb(name, size):
    """
    :param name: 保存图片的名字
    :param size: 长和宽的元组
    :return: 无
    """
    file, ext = os.path.splitext(name)
    im = Image.open('static/uploads/{}'.format(name))
    im.thumbnail(size)
    im.save("static/uploads/thumbnail/{}_{}*{}.jpg".format(file, size[0], size[1]), "JPEG")