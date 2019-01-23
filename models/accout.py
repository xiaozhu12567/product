from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import exists
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base
from .db import DBSession



session = DBSession()
class User(Base):
    """
    用户表，记录用户相关信息
    """
    __tablename__='users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    createtime = Column(DateTime, default=datetime.now)

    def __repr_(self):
        return '<User(#{}: {})>'.format(self.id, self.name)

    @classmethod
    def is_exists(cls, username):
        return session.query(exists().where(User.name == username)).scalar()


    @classmethod        # 类方法
    def add_user(cls, username, password):
        """
        增加一个用户
        :param uesrname:
        :param password:
        :return:
        """
        user = User(name=username, password=password)
        session.add(user)
        session.commit()

    @classmethod
    def get_password(cls, username):
        user = session.query(User).filter_by(name=username).first()
        if user:
            return user.password
        else:
            return ''


class Post(Base):
    """
    用户图片信息
    """
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    img_url = Column(String(80))
    thumb_url = Column(String(100))

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref='posts', uselist=False, cascade='all')

    def __repr_(self):
        return '<Post(#{})>'.format(self.id)


# if __name__ == '__main__':
#     Base.metadata.create_all()