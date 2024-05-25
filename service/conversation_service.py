import datetime
import logging
import uuid

from sqlalchemy.orm import Session

from component.DB_engine import engine
from db.create_db import Conversation
from message_model.request_model.conversation_model import NewConv


async def new_conversation(nc: NewConv):
    """
    用户建立新的对话：
    1. 为新的对话生成一个全局唯一的
    """
    conv_id = uuid.uuid4().hex

    try:
        with Session(engine) as session:
            session.add(Conversation(id=conv_id, conv_name=nc.conv_name, create_time=datetime.datetime.utcnow(), user_id=nc.user_id))
            session.commit()
        logging.info(f"{nc.user_id} 创建了会话 {conv_id} 会话名{nc.conv_name}")
    except Exception as e:
        logging.error(f"{nc.user_id} 创建会话失败 {e}")
        return {"error": f"创建会话失败 {e}"}

    return {"conv_id": conv_id}
