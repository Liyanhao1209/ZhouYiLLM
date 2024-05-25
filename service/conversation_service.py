import datetime
import json
import logging
import uuid

from sqlalchemy.orm import Session

from component.DB_engine import engine
from config.server_config import CHAT_ARGS
from db.create_db import Conversation
from message_model.request_model.conversation_model import NewConv, LLMChat
from message_model.response_model.response import BaseResponse

import requests


async def new_conversation(nc: NewConv) -> BaseResponse:
    """
    用户建立新的对话：
    1. 为新的对话生成一个全局唯一的uuid
    2. 将这个conversation_id插入到数据库中 同时确保外键约束
    """
    conv_id = uuid.uuid4().hex

    try:
        with Session(engine) as session:
            session.add(Conversation(id=conv_id, conv_name=nc.conv_name, create_time=datetime.datetime.utcnow(),
                                     user_id=nc.user_id))
            session.commit()
        logging.info(f"{nc.user_id} 创建了会话 {conv_id} 会话名{nc.conv_name}")
    except Exception as e:
        logging.error(f"{nc.user_id} 创建会话失败 {e}")
        return BaseResponse(code=200, message="会话创建失败", data={"error": f'{e}'})

    return BaseResponse(code=200, message="会话创建成功", data={"conv_id": conv_id})


async def request_llm_chat(ca: LLMChat) -> dict:
    """
    生成llm对话请求
    包含参数有:
    1. query
    2. conv_id
    3. history_len
    4. model_name
    5. temperature
    6. prompt_name
    """
    request_body = {
        "query": ca.query,
        "conversation_id": ca.conv_id,
        "history_len": CHAT_ARGS["history_len"],
        "model_name": CHAT_ARGS["llm_models"][0],
        "temperature": CHAT_ARGS["temperature"],
        "prompt_name": ca.prompt_name
    }

    try:
        response = requests.post(url=CHAT_ARGS["url"], json=request_body)
        print(response.text)
    except Exception as e:
        return {"success": False, "error": f'{e}'}

    if response.ok:
        return {"success": True, "data": json.loads(response.text[len("data: "):].strip())}

    return {"success": False, "error": f'{response.text}'}
