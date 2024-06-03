import datetime
import json
import logging
import uuid
from typing import List, Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from component.DB_engine import engine, record_lock
from component.Online_LLM_client import get_zhipu_client
from config.server_config import CHAT_ARGS, KB_CHAT_ARGS, SE_CHAT_ARGS, ONLINE_LLM_ARGS
from config.template_config import get_mix_chat_prompt, get_online_llm_chat_prompt
from db.create_db import Conversation, Record
from message_model.request_model.conversation_model import NewConv, LLMChat, KBChat, MixChat, SEChat, History, \
    OnlineLLMChat
from message_model.response_model.response import BaseResponse
from util.utils import request, serialize_conversation, serialize_record, stream_response, forward_request_to_kernel

from fastapi.responses import StreamingResponse


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
        return BaseResponse(code=500, msg="会话创建失败", data={"error": f'{e}'})

    return BaseResponse(code=200, msg="会话创建成功", data={"conv_id": conv_id})


async def request_mix_chat(mc: MixChat) -> Any:
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
        return BaseResponse(code=500, msg="大模型请求失败", data={"error": f'{llm_response["error"]}'})

    async def generate_multi_turn_sse():
        # 请求知识库，流式输出docs
        kb_request_body = {
            "query": mc.query,
            "knowledge_base_name": mc.knowledge_base_id if not mc.knowledge_base_id == "-1" else "faiss_zhouyi",
            "top_k": KB_CHAT_ARGS["top_k"],
            "score_threshold": KB_CHAT_ARGS["score_threshold"],
            # "history": "",
            "model_name": CHAT_ARGS["llm_models"][0],
            "temperature": CHAT_ARGS["temperature"],
            "prompt_name": mc.prompt_name,
            "stream": KB_CHAT_ARGS["stream"]
        }
        kb_response = {"data": {}}

        kb_response["data"]["answer"] = ""
        kb_docs = None

        async for data in forward_request_to_kernel(KB_CHAT_ARGS["url"], kb_request_body):
            #符合sse格式
            if "docs" in data:
                # event_data = json.dumps(data)
                event_data = json.dumps({"data":data})
                kb_docs = data
                # print(kb_docs)
                # yield f"{event_data}\n\n"
                yield f"event: message\ndata: {event_data}\n\n"

            elif "answer" in data:
                kb_response["data"]["answer"] = kb_response["data"]["answer"].join(data["answer"])

        # 生成prompt模板
        prompt = get_mix_chat_prompt(question=mc.query, history=await gen_history(mc.conv_id),
                                     answer1=llm_response["data"]["text"], answer2=kb_response["data"]["answer"],
                                     answer3="")  # answer3=online_llm_response["data"]["answer"]

        # 请求大模型
        mix_request_body = {
            "query": prompt,
            "conversation_id": mc.conv_id,
            # "history_len": CHAT_ARGS["history_len"],
            "history_len": -1,
            "model_name": CHAT_ARGS["llm_models"][0],
            "temperature": CHAT_ARGS["temperature"],
            "prompt_name": mc.prompt_name,
            "stream": True
        }

        ma = ""
        #符合sse格式
        async for data in forward_request_to_kernel(CHAT_ARGS["url"], mix_request_body):
            # event_data = json.dumps(data)
            event_data = json.dumps({"data":data})
            ma = ma + data["text"]
            # yield f"{event_data}\n\n"
            yield f"event: message\ndata: {event_data}\n\n"

        # 确保问题和回答原子性地入库
        with record_lock:
            add_record_to_conversation(mc.conv_id, mc.query, False)
            add_record_to_conversation(mc.conv_id, json.dumps({"answer": ma, "docs": kb_docs}, ensure_ascii=False),
                                       True)

    sse = StreamingResponse(generate_multi_turn_sse(), media_type="text/event-stream")
    sse.headers["Cache-Control"] = "no-cache"
    sse.headers["Connection"] = "keep-alive"

    return sse


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
        # "history_len": CHAT_ARGS["history_len"],
        "history_len": -1,
        "model_name": CHAT_ARGS["llm_models"][0],
        "temperature": CHAT_ARGS["temperature"],
        "prompt_name": ca.prompt_name
    }

    return await request(url=CHAT_ARGS["url"], request_body=request_body, prefix="data: ")


async def request_knowledge_base_chat(kb: KBChat) -> Any:
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
        # "history": "",
        "model_name": CHAT_ARGS["llm_models"][0],
        "temperature": CHAT_ARGS["temperature"],
        "prompt_name": kb.prompt_name,
        "stream": KB_CHAT_ARGS["stream"]
    }

    # 获取历史记录
    # history = await gen_history(conv_id=kb.conv_id)
    # request_body["history"] = history  #json.dumps([h.dict() for h in history])

    if not KB_CHAT_ARGS["stream"]:
        return await request(url=KB_CHAT_ARGS["url"], request_body=request_body, prefix="data: ")
    else:
        return await stream_response(url=KB_CHAT_ARGS["url"], request_body=request_body)


async def request_search_engine_chat(sc: SEChat) -> Any:
    # todo:duckduckgo搜索引擎一直超时 需要解决  (别解决了，这个功能0.2.x版本不支持)
    """
    生成搜索引擎对话请求
    1. query
    2. search_engine_name
    3. top_k
    4. history
    5. model_name
    6. temperature
    7. prompt_name
    """
    request_body = {
        "query": sc.query,
        "search_engine_name": sc.search_engine_name,
        "top_k": KB_CHAT_ARGS["top_k"],
        # "history": "",
        "model_name": CHAT_ARGS["llm_models"][0],
        "temperature": CHAT_ARGS["temperature"],
        "prompt_name": sc.prompt_name,
        "stream": SE_CHAT_ARGS["stream"]
    }

    # 获取历史记录
    # history = await gen_history(conv_id=sc.conv_id)
    # request_body["history"] = history
    if SE_CHAT_ARGS["stream"]:
        return await request(url=SE_CHAT_ARGS["url"], request_body=request_body, prefix="data: ")
    else:
        return await stream_response(url=SE_CHAT_ARGS["url"], request_body=request_body)


async def request_online_llm(olc: OnlineLLMChat) -> BaseResponse:
    try:
        response = get_zhipu_client().chat.completions.create(
            model=ONLINE_LLM_ARGS['model'][0],
            messages=[
                {
                    "role": "user",
                    "content": get_online_llm_chat_prompt(olc.query)
                }
            ]
        )
    except Exception as e:
        return BaseResponse(code=500, msg="在线大模型请求失败", data={"error": f'{e}'})

    return BaseResponse(code=200, msg="在线大模型请求成功", data={"answer": response.choices[0].message.content})


async def get_user_conversations(user_id: str) -> BaseResponse:
    try:
        with Session(engine) as session:
            conversations = session.query(Conversation).filter(Conversation.user_id == user_id).all()
        return BaseResponse(code=200, msg='获取会话列表成功',
                            data={"conversations": [serialize_conversation(c) for c in conversations]})
    except Exception as e:
        return BaseResponse(code=500, msg='获取会话列表失败', data={'error': f'{e}'})


async def get_conversation_record(conv_id: str) -> BaseResponse:
    try:
        records = await get_conversation_history(conv_id)
        return BaseResponse(code=200, msg=f'获取会话{conv_id}记录成功',
                            data={'records': [serialize_record(r) for r in records]})
    except Exception as e:
        return BaseResponse(code=500, msg=f'获取会话{conv_id}记录失败', data={'error': f'{e}'})


async def gen_history(conv_id: str) -> List[History]:
    records = await get_conversation_history(conv_id)
    if len(records) % 2 != 0:
        return []
    history = []
    for i in range(0, len(records), 2):
        history.append(
            History.from_data({
                "role": "user",
                "content": records[i].content
            })
        )

        history.append(
            History.from_data({
                "role": "assistant",
                "content": records[i + 1].content
            })
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
        result = session.query(Record).filter(Record.conv_id == conv_id).order_by(Record.id).all()
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
