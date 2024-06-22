import uuid

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from db.create_db import User

if __name__ == '__main__':
    engine = create_engine(f'sqlite:///./zhouyi_web.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    for i in range(1, 1001):
        user_id = str(uuid.uuid4().hex)
        user = User(
            id=user_id,
            email=f"{i}@qq.com",
            password="af333d1adb38a5ea7356363ac090baa7",
            name='',
            is_active=True,
            age=21,
            sex="male",
            description=''
        )
        session.add(user)

    try:
        session.commit()
        print("Fake User Complete")
    except IntegrityError as e:
        session.rollback()
        print(f"发生错误：{e}")
    finally:
        session.close()
