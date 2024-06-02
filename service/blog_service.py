import logging
import uuid
from datetime import datetime

from db.create_db import Blog
from message_model.request_model.blog_model import BlogModel
from message_model.response_model.response import BaseResponse

from sqlalchemy.orm import Session
from component.DB_engine import engine
from util.utils import serialize_blog


def add_blog(blog: BlogModel) -> BaseResponse:
    try:
        with Session(engine) as session:
            time = datetime.now()

            if blog.blog_id is None or blog.blog_id == '':
                blog_id = uuid.uuid4().hex
                session.add(
                    Blog(id=blog_id, title=blog.title, content=blog.content, create_time=time, user_id=blog.user_id))
            else:
                # 用户已经存在
                blog_id = blog.blog_id
                b = session.query(Blog).filter(Blog.id == blog_id).first()
                b.content = blog.content
                b.title = blog.title
            session.commit()
    except Exception as e:
        print(e)
        logging.info(f'user_id为{blog.user_id}的用户创建博客失败, time{time}')
        return BaseResponse(msg="创建失败")
    return BaseResponse(code=200, msg='添加成功', data={'blog_id': blog_id})


def get_blog(user_id: str) -> BaseResponse:
    try:
        with Session(engine) as session:
            result = session.query(Blog).filter(Blog.user_id == user_id).all()

    except Exception as e:
        print(e)
        return BaseResponse(msg="查询失败")
    return BaseResponse(code=200, msg='查询成功', data={'blog_list': [serialize_blog(blog) for blog in result]})


def delete_blog(blog_id: str) -> BaseResponse:
    try:
        with Session(engine) as session:
            session.query(Blog).filter(Blog.id == blog_id).delete()
            session.commit()
    except Exception as e:
        print(e)
        return BaseResponse(msg="删除失败")
    return BaseResponse(code=200, msg='删除成功')
