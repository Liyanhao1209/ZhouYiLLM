import logging
from threading import Lock

from sqlalchemy import create_engine, event

from config.database_config import SQLITE_CONNECTION

db_lock = Lock()
engine = None


# 初始化数据库连接
def init_db_conn():
    global engine, db_lock
    db_lock.acquire()
    engine = create_engine(f'sqlite:///{SQLITE_CONNECTION["location"]}')

    # 注册连接监听 连接时开启外键约束(默认不开启)
    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        logging.info("Sqlite数据库已开启外键约束")
        cursor.close()

    db_lock.release()
