from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .db import Base

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


# if __name__ == '__main__':
#     Base.metadata.create_all()