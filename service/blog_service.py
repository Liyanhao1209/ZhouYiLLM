import logging
import os
import uuid
from datetime import datetime
import requests
from fastapi import UploadFile
from db.create_db import Blog
from message_model.request_model.blog_model import BlogModel
from message_model.response_model.response import BaseResponse
from service.knowledge_base_service import upload_knowledge_files
from config.knowledge_base_config import KB_ARGS, FILE_ARGS, DOC_ARGS
from sqlalchemy.orm import Session
from component.DB_engine import engine
from util.utils import serialize_blog


async def add_blog(blog: BlogModel) -> BaseResponse:
    """
    添加博客
    """
    global res
    try:
        with Session(engine) as session:
            time = datetime.now()

            if blog.blog_id is None or blog.blog_id == '':
                blog_id = uuid.uuid4().hex
                session.add(
                    Blog(id=blog_id, title=blog.title, content=blog.content, create_time=time, user_id=blog.user_id))
            else:
                # 博客已经存在
                blog_id = blog.blog_id
                b = session.query(Blog).filter(Blog.id == blog_id).first()
                b.content = blog.content
                b.title = blog.title
            session.commit()
    except Exception as e:
        print(e)
        logging.info(f'user_id为{blog.user_id}的用户创建博客失败, time{time}')
        return BaseResponse(msg="创建失败")

    # 文件保存本地
    # 上传知识库
    if blog.save_to_kb:
        filename = save_md(blog.title, blog.content)
        file = open(filename, "rb")
        files = {'files': (blog.title + '.md', file)}
        form_data = {
            'knowledge_base_name': KB_ARGS["default_kb"],
            'override': DOC_ARGS["override_custom_docs"],
            'to_vector_store': DOC_ARGS["to_vector_store"],
            'chunk_size': DOC_ARGS["chunk_size"],
            'chunk_overlap': DOC_ARGS["overlap_size"],
            'zh_title_enhance': DOC_ARGS["zh_title_enhance"],
            'docs': DOC_ARGS["docs"],
            'not_refresh_vs_cache': DOC_ARGS["not_refresh_vs_cache"]
        }
        try:
            response = requests.post(DOC_ARGS['url'], files=files, data=form_data)
        except Exception as e:
            return BaseResponse(code=500, msg="上传文件失败", data={"error": f'{e}'})

        print(response.json())
    return BaseResponse(code=200, msg='添加成功', data={'blog_id': blog_id})


def get_blog(user_id: str) -> BaseResponse:
    """获取博客列表"""
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


def blog(blog_id: str) -> BaseResponse:
    """
    获取博客内容
    """
    try:
        with Session(engine) as session:
            result = session.query(Blog).filter(Blog.id == blog_id).first()
    except Exception as e:
        print(e)
        return BaseResponse(msg="查询失败")
    return BaseResponse(code=200, msg='查询成功', data=serialize_blog(result))


def save_md(title: str, content: str):
    """将md文件存本地"""
    filename = title + '.md'
    path = os.getcwd() + FILE_ARGS["relative_path"]
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + filename, 'w', encoding='utf-8') as f:
        f.write(content)
        f.close()
    return path + filename
