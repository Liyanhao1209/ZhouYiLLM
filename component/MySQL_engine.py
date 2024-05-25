from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from threading import Lock

from config.database_config import SQLITE_CONNECTION

db_lock = Lock()
engine = None


# 初始化数据库连接
def init_db_conn():
    global engine, Session, db_lock
    db_lock.acquire()
    engine = create_engine(f'sqlite:///{SQLITE_CONNECTION}')
    Session = sessionmaker(bind=engine)
    db_lock.release()


# 获取数据库会话
def get_db_session():
    global db_lock, Session
    db_lock.acquire()
    session = Session()
    db_lock.release()
    return session
