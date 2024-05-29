import datetime
import uuid

from sqlalchemy.orm import Session

import db.create_db
from component.DB_engine import engine
from config.knowledge_base_config import KB_ARGS
from message_model.request_model.knowledge_base_model import KnowledgeBase
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

