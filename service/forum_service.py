import datetime
import uuid

from sqlalchemy.orm import Session

from component.DB_engine import engine
from db.create_db import Blog, User, Comment
from message_model.request_model.forum_model import CommentModel
from message_model.response_model.response import BaseResponse
from util.utils import serialize_blog, blog_user_to_dict, serialize_comment, serialize_comment_user


def get_all_blogs() -> BaseResponse:
    """
    获取论坛上所有的博客列表
    """
    try:
        with Session(engine) as session:
            # 按事件降序排列
            # 需要添加博客的作者信息

            res = session.query(Blog.id, Blog.title, Blog.content, Blog.create_time, User.id, User.name).join(User,
                                                                                                              User.id == Blog.user_id).order_by(
                Blog.create_time.desc()).all()
    except Exception as e:
        print(e)
        return BaseResponse(code=500, message=str(e))
    return BaseResponse(code=200, msg='success', data=[blog_user_to_dict(b) for b in res])


def add_comment(comment: CommentModel) -> BaseResponse:
    comment_id = uuid.uuid4().hex
    now = datetime.datetime.now()
    try:
        with Session(engine) as session:
            session.add(Comment(id=comment_id,
                                content=comment.comment,
                                create_time=now,
                                user_id=comment.user_id,
                                blog_id=comment.blog_id))
            session.commit()
        return BaseResponse(code=200, msg='success', data={comment_id: comment_id})
    except Exception as e:
        print(e)
        return BaseResponse(code=500, message=str(e))


def get_comment(blog_id: str) -> BaseResponse:
    """
    获取一个博客的评论
    """
    try:
        with Session(engine) as session:
            res = session.query(Comment, User.name).join(User, Comment.user_id == User.id).filter(
                Comment.blog_id == blog_id).all()
    except Exception as e:
        print(e)
        return BaseResponse(code=500, message=str(e))
    return BaseResponse(code=200, msg='success', data=[serialize_comment_user(comment) for comment in res])


def delete_comment(blog_id: str, user_id: str) -> BaseResponse:
    """
    删除博客的评论，注意权限判断
    """
    try:
        with Session(engine) as session:
            res = session.query(Comment).filter(Comment.blog_id == blog_id).first()
            if res is None:
                return BaseResponse(code=400, msg='没有这个评论')
            if res.user_id == user_id:  # 删除者是评论本人
                session.delete(res)
                session.commit()
                return BaseResponse(code=200, msg='success')
            blog = session.query(Blog).filter(Blog.id == blog_id).first()
            if blog.user_id == user_id:  # 删除者是博客作者
                session.delete(res)
                session.commit()
                return BaseResponse(code=200, msg='success')
            return BaseResponse(code=400, msg='你没有删除的权限')
    except Exception as e:
        print(e)
        return BaseResponse(code=500, msg=str(e))
