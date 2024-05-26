from typing import List

from fastapi import FastAPI

from message_model.response_model.response import BaseResponse
from routers.mount_routers import routers_mount_interface
from service.conversation_service import new_conversation, request_llm_chat, request_knowledge_base_chat


class ConversationRouter(routers_mount_interface):
    def __init__(self, prefix: str, tag: List[str]):
        super().__init__(prefix, tag)

    def mount(self, app: FastAPI):
        app.post(self.generate_route_path(["new-conversation"]), tags=self.tag, response_model=BaseResponse,
                 summary="用户创建新会话")(new_conversation)
        app.post(self.generate_route_path(["llm-chat"]), tags=self.tag, summary="请求LLM聊天接口")(request_llm_chat)
        app.post(self.generate_route_path(["knowledge-base-chat"]), tags=self.tag,
                 summary="请求知识库聊天接口")(request_knowledge_base_chat)
