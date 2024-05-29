import datetime
import json
import uuid

import requests
from sqlalchemy.orm import Session

import db.create_db
from component.DB_engine import engine
from config.knowledge_base_config import KB_ARGS, DOC_ARGS
from message_model.request_model.knowledge_base_model import KnowledgeBase, KBFile
from message_model.response_model.response import BaseResponse
from util.utils import request


async def create_knowledge_base(kb: KnowledgeBase) -> BaseResponse:
    kb_id = uuid.uuid4().hex

    try:
        with Session(engine) as session:
            session.add(db.create_db.KnowledgeBase(id=kb_id, name=kb.kb_name, description=kb.desc,
                                                   create_time=datetime.datetime.utcnow(), user_id=kb.user_id))
            session.commit()
    except Exception as e:
        return BaseResponse(code=500, msg="创建知识库失败", data={"error": f'{e}'})

    """
    创建知识库
    1. knowledge_base_name
    2. vector_store_type
    3. embed_model
    """
    request_body = {
        "knowledge_base_name": kb_id,
        "vector_store_type": KB_ARGS["vector_store_type"],
        "embed_model": KB_ARGS["embed_model"],
    }

    response = await request(url=KB_ARGS['url'], request_body=request_body, prefix="")

    if response["success"]:
        return BaseResponse(code=200, msg="创建知识库成功", data={"kb_id": kb_id})

    return BaseResponse(code=500, msg="创建知识库失败", data={"error": response["error"]})


async def upload_knowledge_files(kbf: KBFile) -> BaseResponse:
    # 表单参数
    form_data = {
        'knowledge_base_name': kbf.knowledge_base_id,
        'override': DOC_ARGS["override_custom_docs"],
        'to_vector_store': DOC_ARGS["to_vector_store"],
        'chunk_size': DOC_ARGS["chunk_size"],
        'chunk_overlap': DOC_ARGS["overlap_size"],
        'zh_title_enhance': DOC_ARGS["zh_title_enhance"],
        'docs': DOC_ARGS["docs"],
        'not_refresh_vs_cache': DOC_ARGS["not_refresh_vs_cache"]
    }

    files = {'files': kbf.files}

    response = requests.post(DOC_ARGS['url'], files=files, data=form_data)

    if response.ok:
        return BaseResponse(code=200, msg="上传文件成功", data={
            "failed_files": json.loads(response.text[response.text.find('{'):response.text.rfind('}') + 1])[
                "failed_files"]})


async def get_user_kbs(user_id: str) -> BaseResponse:
    try:
        with Session(engine) as session:
            user_kbs = session.query(db.create_db.KnowledgeBase).filter(
                db.create_db.KnowledgeBase.user_id == user_id).all()
        return BaseResponse(code=200, msg="获取知识库成功", data={"user_kbs": [serialize_knowledge_base(kb) for kb in user_kbs]})
    except Exception as e:
        return BaseResponse(code=500, msg="获取知识库失败", data={"error": f'{e}'})


def serialize_knowledge_base(kb: db.create_db.KnowledgeBase) -> dict:
    return {
        'id': kb.id,
        'name': kb.name,
        'create_time': kb.create_time.isoformat() if kb.create_time else None,
        'user_id': kb.user_id,
    }
