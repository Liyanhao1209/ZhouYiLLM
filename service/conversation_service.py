import logging
import uuid

from message_model.request_model.conversation_model import NewConv


async def new_conversation(nc: NewConv):
    """
    用户建立新的对话：
    1. 为新的对话生成一个全局唯一的
    """
    conv_id = uuid.uuid4().hex
    logging.log(logging.INFO, f"{nc.user_id} 创建了会话 {conv_id} 会话名{nc.conv_name}")

    # todo: 将用户与会话的关系插入数据库
    return {"conv_id": conv_id}
