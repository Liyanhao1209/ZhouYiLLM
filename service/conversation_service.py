import datetime
import json
import logging
import uuid
from typing import List

import requests
from sqlalchemy import func
from sqlalchemy.orm import Session

from component.DB_engine import engine
from config.server_config import CHAT_ARGS, KB_CHAT_ARGS
from config.template_config import get_mix_chat_prompt
from db.create_db import Conversation, Record
from message_model.request_model.conversation_model import NewConv, LLMChat, KBChat, MixChat
from message_model.response_model.response import BaseResponse


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


async def request(url: str, request_body: dict, prefix: str) -> dict:
    try:
        response = requests.post(url=url, json=request_body)
        print(response.text)
    except Exception as e:
        return {"success": False, "error": f'{e}'}

    if response.ok:
        return {"success": True, "data": json.loads(response.text[len(prefix):].strip())}

    return {"success": False, "error": f'{response.text}'}


async def request_mix_chat(mc: MixChat) -> BaseResponse:
    """
    混合对话
    1. 先请求大模型以自身能力给出解答
    2. 再请求大模型检索知识库给出解答
    3. 最后请求大模型通过询问搜索引擎给出解答
    4. 最终将解答融合在一起返回
    """
    # 先请求大模型以自身能力给出解答
    llm_response = await request_llm_chat(LLMChat(query=mc.query, conv_id=mc.conv_id))
    if not llm_response["success"]:
        return BaseResponse(code=200, message="大模型请求失败", data={"error": f'{llm_response["error"]}'})

    # 请求知识库
    kb_response = await request_knowledge_base_chat(KBChat(query=mc.query, conv_id=mc.conv_id))
    if not kb_response["success"]:
        return BaseResponse(code=200, message="知识库请求失败", data={"error": f'{kb_response["error"]}'})

    # 请求搜索引擎
    search_response = await request_search_engine_chat()

    # 生成prompt
    prompt = get_mix_chat_prompt(question=mc.query, history=gen_history(mc.conv_id),
                                 answer1=llm_response["data"]["text"], answer2=kb_response["data"]["answer"],
                                 answer3="")

    # 请求大模型
    response = await request_llm_chat(LLMChat(query=prompt, conv_id=mc.conv_id, prompt_name=mc.prompt_name))

    return BaseResponse(code=200, message="混合对话请求成功", data={"answer": response["data"]["text"]})


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

    return await request(url=CHAT_ARGS["url"], request_body=request_body, prefix="data: ")


async def request_knowledge_base_chat(kb: KBChat) -> dict:
    """
    生成知识库对话请求
    参数：
    1. query
    2. knowledge_base_name
    3. top_k
    4. score_threshold
    5. history:List[History]
    6. model_name
    7. temperature
    8. prompt_name
    """
    request_body = {
        "query": kb.query,
        "knowledge_base_name": kb.knowledge_base_id if not kb.knowledge_base_id == "-1" else "faiss_zhouyi",
        "top_k": KB_CHAT_ARGS["top_k"],
        "score_threshold": KB_CHAT_ARGS["score_threshold"],
        "history": "",
        "model_name": CHAT_ARGS["llm_models"][0],
        "temperature": CHAT_ARGS["temperature"],
        "prompt_name": kb.prompt_name
    }

    # 获取历史记录
    history = await gen_history(conv_id=kb.conv_id)
    request_body["history"] = history

    return await request(url=KB_CHAT_ARGS["url"], request_body=request_body, prefix="data: ")


async def request_search_engine_chat() -> dict:
    return {}


async def gen_history(conv_id: str) -> List[List[dict]]:
    records = await get_conversation_history(conv_id)
    history = []
    for i in range(0, len(records), 2):
        history.append(
            [
                {
                    "role": "user",
                    "content": records[i].content
                },
                {
                    "role": "assistant",
                    "content": records[i + 1].content
                }
            ]
        )
    return history


def max_id_in_record() -> int:
    with Session(engine) as session:
        result = session.query(func.max(Record.id)).scalar()
        if result:
            return result
        else:
            return 0


# 将聊天记录插入数据库
def add_record_to_conversation(conv_id: str, text: str, is_ai: bool) -> None:
    with Session(engine) as session:
        session.add(Record(id=max_id_in_record() + 1, content=text, is_ai=is_ai, conv_id=conv_id))
        session.commit()


# 查询某个会话的所有聊天记录
async def get_conversation_history(conv_id: str) -> List:
    with Session(engine) as session:
        result = session.query(Record).filter(Record.conv_id == conv_id).all()
        return result


# 查询一个用户的所有聊天记录
async def get_user_chat_records(user_id: str) -> dict:
    res = {}
    with Session(engine) as session:
        conversations = session.query(Conversation).filter(Conversation.user_id == user_id).all()
        for conv in conversations:
            conv_records = get_conversation_history(conv.id)
            res[conv.id] = conv_records

    return res
