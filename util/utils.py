import json

import requests
import db


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
