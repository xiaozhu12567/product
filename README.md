# product
图片上传和展示
上传表单和文件保存
self.request.files的使用
    def post(self, *args, **kwargs):
        file_list = self.request.files.get('newimg', None)
        for upload in file_list:
            name = upload['filename']
            content = upload['body']

        with open('static/uploads/{}'.format(name), 'wb') as f:
            f.write(content)
python操作文件，写入文件

用简单的目录检索来展示
使用python标准库glob

缩略图生成
pip install pillow
使用pil
from PIL import Image
for img in imgs:
    file, ext = os.path.slitext(img)
    im = Image.open(img)
    im.thumbnail((200,200))
    im.save("{}_{}*{}.jpg".format(file, 200, 200), "JPEG")
  
    
配置alembic，sqlalchemy版本迁移
1) pip安装包
pip install pymysql
pip install sqlalchemy
pip install alembic

2）alembic初始化
切换到项目目录下，执行初始化
alembic init alembic

3）修改配置文件alembic.ini设置数据库连接
sqlalchemy.url = mysql+pymysql://root:123.coM@127.0.0.1/product

4）在env.py中设置，将target_metadata赋值成数据库中的元数据
import sys
from os.path import abspath, dirname
root = dirname(dirname(abspath(__file__)))  # 拿到项目根目录
sys.path.append(root)
from models.accout import Base
target_metadata = Base.metadata

5）配置完成后，执行
alembic revision --autogenerate -m "create_user_table"
alembic upgrade head

Bootstrap4
https://code.z01.com/v4
https://code.z01.com/v4/docs/
https://www.bootcdn.cn
http://www.fontawesome.com.cn/get-started/
https://fontawesome.com/v4.7.0/
https://www.bootcss.com
fontawesome.io
