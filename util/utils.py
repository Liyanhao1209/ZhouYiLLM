import json
from typing import AsyncIterable

import requests
from aiohttp import ClientSession
from fastapi.responses import StreamingResponse

import db


async def forward_request_to_kernel(url: str, request_body: dict) -> AsyncIterable:
    async with ClientSession() as session:
        async with session.post(url, json=request_body) as response:
            if response.status != 200:
                raise Exception(f"Failed to get response from knowledge base: {response.text()}")

            async for chunk in response.content:
                line = chunk.decode()
                if line.startswith("data: "):
                    # 提取data字段后面的内容，并去除尾部的换行符
                    json_data = line[len("data: "):].strip()
                    # 产生JSON数据
                    yield json.loads(json_data)


async def stream_response(url: str, request_body: dict) -> StreamingResponse:
    async def generate_sse():
        async for data in forward_request_to_kernel(url, request_body):
            event_data = json.dumps(data)
            yield f"{event_data}\n\n"

    response = StreamingResponse(generate_sse(), media_type="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"

    return response


async def request(url: str, request_body: dict, prefix: str) -> dict:
    try:
        response = requests.post(url=url, headers={"Content-Type": "application/json"}, json=request_body)
        # print(response.text)
        text = response.text[response.text.find('{'):response.text.rfind('}') + 1]
        print(text)
    except Exception as e:
        return {"success": False, "error": f'{e}'}

    if response.ok:
        return {"success": True, "data": json.loads(text)}

    return {"success": False, "error": f'{response.text}'}


def serialize_knowledge_base(kb: db.create_db.KnowledgeBase) -> dict:
    return {
        'id': kb.id,
        'name': kb.name,
        'create_time': kb.create_time.isoformat() if kb.create_time else None,
        'user_id': kb.user_id,
    }


def serialize_conversation(conv: db.create_db.Conversation) -> dict:
    return {
        'id': conv.id,
        'conv_name': conv.conv_name,
        'create_time': conv.create_time.isoformat() if conv.create_time else None,
        'user_id': conv.user_id
    }


def serialize_record(record: db.create_db.Record) -> dict:
    return {
        'id': record.id,
        'content': record.content,
        'is_ai': record.is_ai,
        'conv_id': record.conv_id
    }
