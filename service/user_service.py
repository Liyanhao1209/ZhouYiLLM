import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from component.DB_engine import engine
from db.create_db import User  # 假设User模型已经定义在db.models模块中，包含username和password字段
from message_model.request_model.user_model import RegisterForm

app = FastAPI()


@app.post("/register")
async def register_user(register_form: RegisterForm):
    """用户注册接口"""
    conv_id = uuid.uuid4().hex
    session = Session(bind=engine)
    try:
        # 检查用户名是否已存在
        existing_user = session.query(User).filter(User.email == register_form.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="用户名已存在")

        # 创建新用户并添加到数据库
        new_user = User(id=conv_id, email=register_form.email, password=register_form.password, name="", is_active=True,
                        age=0, sex="0", description="")
        print(new_user)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)  # 获取新插入记录的id等信息

        return {"code": 200, "message": "注册成功", "data": {"user_id": new_user.id}}
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail="注册失败，可能是由于数据库完整性约束")
    finally:
        session.close()


@app.post("/login")
async def login_user():
    pass
