import random
import uuid
from datetime import timedelta
from hashlib import md5

from fastapi import HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from config.server_config import JWT_ARGS
from component.DB_engine import engine
from component.email_server import send_email
from component.redis_server import get_redis_instance
from component.token_server import create_access_token, get_current_active_user
from db.create_db import User  # User模型已经定义在db.models模块中，包含username和password字段
from message_model.request_model.user_model import RegisterForm, LoginForm, InfoForm
from message_model.response_model.response import BaseResponse


async def register_user(register_form: RegisterForm):
    """用户注册接口"""
    conv_id = uuid.uuid4().hex
    session = Session(bind=engine)
    try:
        # 检查用户名是否已存在
        existing_user = session.query(User).filter(User.email == register_form.email).first()
        if existing_user:
            return BaseResponse(code=400, msg='账号已存在')

        redis = get_redis_instance()
        judge = redis.get(register_form.email)
        if not judge:
            return BaseResponse(code=401, msg='验证码未发送')
        captcha_code_str = judge.decode('utf-8')

        if register_form.captcha != captcha_code_str:
            return BaseResponse(code=402, msg='验证码错误')
        # 对密码进行MD5加密
        password_hash = md5(register_form.password.encode('utf-8')).hexdigest()
        new_user = User(id=conv_id, email=register_form.email, password=password_hash, name="", is_active=True,
                        age=0, sex="0", description="")

        session.add(new_user)
        session.commit()
        session.refresh(new_user)  # 获取新插入记录的id等信息

        return {"code": 200, "message": "注册成功", "data": {"user_id": new_user.id}}
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail="注册失败，可能是由于数据库完整性约束")
    finally:
        session.close()

async def update_password(register_form: RegisterForm):
    session = Session(bind=engine)
    try:
        # 根据用户邮箱查询用户
        user = session.query(User).filter(User.email == register_form.email).first()
        if not user:
            return BaseResponse(code=400, msg='账号不存在')

        redis = get_redis_instance()
        judge = redis.get(register_form.email)
        if not judge:
            return BaseResponse(code=401, msg='验证码未发送')
        captcha_code_str = judge.decode('utf-8')

        if register_form.captcha != captcha_code_str:
            return BaseResponse(code=402, msg='验证码错误')
        # 更新用户密码
        password_hash = md5(register_form.password.encode('utf-8')).hexdigest()
        user.password=password_hash
        session.commit()
        return {"code": 200, "message": "密码更新成功"}

    except Exception as e:
        session.rollback()  # 发生异常时回滚事务
        raise HTTPException(status_code=500, detail="密码更新失败，请重试")
    finally:
        session.close()

async def login_user(login_form: LoginForm):
    """
       用户登录接口
       LoginForm 包含 email 和 password 字段
   """
    session = Session(bind=engine)
    try:
        # 根据邮箱查询用户
        user = session.query(User).filter(User.email == login_form.email).first()
        if not user:
            return BaseResponse(code=400, msg='账号不存在')
        # 对用户输入的密码进行MD5加密
        input_password_hash = md5(login_form.password.encode('utf-8')).hexdigest()

        # 验证密码是否正确
        if user.password != input_password_hash:
            return BaseResponse(code=401, msg='密码错误')
        if not user.is_active:
            return BaseResponse(code=402, msg='账号被封禁')
        # 登录成功，在此处生成token
        # token = generate_token(user.email)
        access_token_expires = timedelta(minutes=JWT_ARGS["expire_time"])
        access_token = create_access_token(
            data={"sub": user.email, "index": 0}, expires_delta=access_token_expires  # index索引是0代表用户，1代表管理员
        )
        return {"code": 200, "message": "登录成功",
                "data": {"token": access_token, "token_type": "bearer", "user_id": user.id}}

    except Exception as e:
        return BaseResponse(code=500, msg='登陆失败请重试')
    finally:
        session.close()


async def update_info(info_form: InfoForm, current_user: User = Depends(get_current_active_user)):
    """
       用户更新个人信息接口
       info_form 包含 name ,age,sex,description 字段
    """
    session = Session(bind=engine)
    try:
        # 根据用户ID查询用户
        user = session.query(User).filter(User.id == info_form.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")

        # 更新用户信息
        user.name = info_form.name
        user.age = info_form.age
        user.sex = info_form.sex
        user.description = info_form.description

        session.commit()
        return {"code": 200, "message": "个人信息更新成功"}

    except Exception as e:
        session.rollback()  # 发生异常时回滚事务
        raise HTTPException(status_code=500, detail="个人信息更新失败，请重试")
    finally:
        session.close()


async def send_verification_code(email: str):
    """发送验证码到邮箱并存储到Redis"""
    # 生成6位数字验证码
    code = ''
    for i in range(6):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        code += ch

    send_email(email, '周易大模型验证码', code)  # 发送邮件

    redis = get_redis_instance()
    redis.set(email, code, ex=4000)

    return JSONResponse(content={"detail": "Verification code has been sent to your email."})
