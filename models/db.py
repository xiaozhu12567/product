from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'product'
USERNAME = 'root'
PASSWORD = '123.coM'

db_url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE
)

engine = create_engine(db_url)
Base = declarative_base(engine)         # 是创建所有模型类的基类
DBSession = sessionmaker(bind=engine)          # 用于执行所有sql语句
