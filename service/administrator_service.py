"""
1. 可以查看任意用户的知识库、博客、与大模型的历史会话
2. 可以封禁某用户及其邮箱，并以邮件的方式通知该用户
3. 可以解禁某用户及其邮箱，并以邮件的方式通知该用户
"""
import datetime
import logging
import uuid

from sqlalchemy.orm import Session
from component.DB_engine import engine

from db.create_db import Administrator, Blog, User, Conversation, Record
from message_model.response_model.response import BaseResponse
from message_model.request_model.administrator_model import AdminModel, AdminQueryData


# 获取用户知识库
def see_users_knowledge_base(username: object):
    data = {"username": username}
    return BaseResponse(code=200, msg='请求成功', data=data)


# 添加新管理员
async def add_administrator(admin: AdminModel) -> BaseResponse:
    admin_id = uuid.uuid4().hex
    time = datetime.datetime.now()
    # password需要加密
    try:
        with Session(engine) as session:
            session.add(Administrator(id=admin_id, name=admin.name, password=admin.password))
            session.commit()
        logging.info(f'{time}创建了管理员{admin.name}, id={admin_id}')
    except Exception as e:
        logging.error(f'{time}创建管理员{admin.name}失败')
        return BaseResponse(code=200, message='注册失败', data={'error': str(e)})
    return BaseResponse(code=200, message='注册成功', data={'admin_id': admin_id})


# 获取用户博客
def see_users_blog(user_id: str) -> BaseResponse:
    try:
        with Session(engine) as session:
            result = session.query(Blog).join(User, Blog.user_id == User.id, isouter=True).filter(
                User.id == user_id).all()
    except Exception as e:
        return BaseResponse(code=200, message='操作失败', data={'error': str(e)})
    return BaseResponse(code=200, message="操作成功", data={'result': result})


# 获取用户与模型的对话
def see_users_record(user_id: str) -> BaseResponse:
    try:
        with Session(engine) as session:
            conversations = session.query(Conversation).join(User, Conversation.user_id == User.id,
                                                             isouter=True).filter(
                User.id == user_id).all()
            result = []
            for c in conversations:
                records = session.query(Record).join(Conversation, Record.conv_id == Conversation.id,
                                                     isouter=True).all()
                result.append(records)
    except Exception as e:
        return BaseResponse(code=200, message='查询失败！', data={'error': str(e)})
    return BaseResponse(code=200, message='查询成功！', data={'result': result})


def blocked_user(user_id: str) -> BaseResponse:
    """
    封禁某用户及其邮箱，并以邮件的方式通知该用户
    """
    with Session(engine) as session:
        user = session.query(User).filter(User.id == user_id).one()
        if user is None:
            return BaseResponse(code=200, message='用户不存在！', data={'error': '用户不存在'})
        if not user.is_active:
            return BaseResponse(code=200, message='用户已经被封禁！', data={'error': '用户已经被封禁'})
        user.is_active = False
        session.commit()

    
