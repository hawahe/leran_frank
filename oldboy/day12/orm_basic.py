import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:Bibolang1@localhost/oldboydb",
                       encoding='utf-8',echo = True)

Base = declarative_base() # 生成orm基类


class User(Base):
    __tablename__ = 'user' #表名
    id = Column(Integer,primary_key=True)
    name = Column(String(32))
    password = Column(String(64))

Base.metadata.create_all(engine) #创建表结构

Session_class = sessionmaker(bind=engine) #创建与数据库的会话session class，注意，这里返回给session的诗歌class，不是实例
Session = Session_class() # 生成session实例

user_obj = User(name="alex",password="alex3714") #生成你要创建的数据对象
user_obj2 = User(name="jack",password="122")

print(user_obj.name,user_obj.id) #此事还没创建对象呢，不信你打印一下id发现还是None

Session.add(user_obj) #把要创建的数据对象添加到这个session里，一会儿统一创建
Session.add(user_obj2)

print(user_obj.name,user_obj.id) #此时也依然没有创建

Session.commit() # 现在才统一提交，创建数据

