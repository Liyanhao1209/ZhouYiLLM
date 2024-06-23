import datetime
import uuid

from sqlalchemy.orm import Session

from component.DB_engine import engine
from db.create_db import Blog, User, Comment, BlogStars
from message_model.request_model.forum_model import CommentModel
from message_model.response_model.response import BaseResponse
from sqlalchemy import exists
from util.utils import serialize_blog, blog_user_to_dict, serialize_comment, serialize_comment_user, \
    serialize_stars_blog


async def get_all_blogs() -> BaseResponse:
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
            res_data = [blog_user_to_dict(b) for b in res]
            for blog in res_data:
                stmt = exists().where(BlogStars.blog_id == blog['id'],
                                      BlogStars.user_id == blog['user_id'])
                is_starred = session.query(stmt).scalar()
                blog.update({"is_starred": is_starred})

    except Exception as e:
        print(e)
        return BaseResponse(code=500, msg=str(e))
    return BaseResponse(code=200, msg='success', data=res_data)


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
    return BaseResponse(code=200, msg='success',
                        data={'comment_list': [serialize_comment_user(comment) for comment in res]})


def delete_comment(comment_id: str, blog_id: str, user_id: str) -> BaseResponse:
    """
    删除博客的评论，注意权限判断
    """
    try:
        with Session(engine) as session:
            res = session.query(Comment).filter(Comment.id == comment_id).first()
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


def star_unstar_blog(user_id: str, blog_id: str) -> BaseResponse:
    """收藏一个博客，或者取消收藏一个博客"""
    try:
        with Session(engine) as session:
            res = session.query(BlogStars).filter(BlogStars.user_id == user_id).filter(
                BlogStars.blog_id == blog_id).first()
            if res is None:
                session.add(BlogStars(user_id=user_id, blog_id=blog_id))
                session.commit()
                return BaseResponse(code=200, msg='收藏成功', data=True)
            else:
                session.delete(res)
                session.commit()
                return BaseResponse(code=200, msg='取消收藏', data=False)
    except Exception as e:
        print(e)
        return BaseResponse(code=500, msg=str(e))


def get_star_blog(user_id: str) -> BaseResponse:
    try:
        with Session(engine) as session:
            res = session.query(BlogStars, Blog).join(Blog, Blog.id == BlogStars.blog_id).filter(
                BlogStars.user_id == user_id).all()
            s_res = [serialize_stars_blog(i) for i in res]
            for blog in s_res:
                stmt = exists().where(BlogStars.blog_id == blog['id'],
                                      BlogStars.user_id == blog['user_id'])
                is_starred = session.query(stmt).scalar()
                blog.update({"is_starred": is_starred})
            return BaseResponse(code=200, msg='ok', data={'star_blog_list': s_res})
    except Exception as e:
        print(e)
        return BaseResponse(code=500, msg=str(e))
