# 首先，sqlalchemy和flask_sqlalchemy并不一样
# SQLAlchemy：一个功能强大、灵活的 SQL 工具包和 ORM，适用于任何 Python 应用
# Flask-SQLAlchemy：一个专门为 Flask 框架设计的扩展，简化了配置和集成过程，便于在 Flask 应用中使用 SQLAlchemy
import vs_sql_config
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(vs_sql_config.DATABASE_URL) # 创建引擎，连接到 sqlite 文件
Session = sessionmaker(bind=engine) # 创建会话工厂，用于创建会话对象
Base = declarative_base() # 创建申明性基类

# 定义映射类，对应数据库中的表
class User(Base):
    __tablename__ = 'users'   # 指定表名
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    gender = Column(String(6), nullable=False)
    
def add_users(session, users_data):
    session.add_all(users_data)
    session.commit() # 只有对数据库进行操作时才需要提交
    print(f"\nsuccessfully added {len(users_data)} users")

def query_users(session, user_ids):
    users = session.query(User).filter(User.id.in_(user_ids)).all()
    return users

def run():
    Base.metadata.create_all(engine) # 创建表
    session = Session() # 创建会话
    try:
        new_users = [User(id=33629,name='Alice', email='alice@example.com', gender='female'),
                    User(id=11224,name='Bob', email='bob@example.com', gender='male')]
        add_users(session, new_users)
        users = query_users(session, [11224,33629])
        for user in users:
            print(f"User:{user.name}, Email:{user.email}")
    except Exception as e:
        print(e)
    finally:
        session.close() # 关闭会话

if __name__ == '__main__':
    run()

