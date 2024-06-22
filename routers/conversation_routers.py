from typing import List

from fastapi import FastAPI

from message_model.response_model.response import BaseResponse
from routers.mount_routers import routers_mount_interface
from service.conversation_service import new_conversation, request_llm_chat, request_knowledge_base_chat, \
    request_mix_chat, request_search_engine_chat, get_user_conversations, get_conversation_record, request_online_llm, \
    delete_user_conversation, stop_llm_chat


class ConversationRouter(routers_mount_interface):
    def __init__(self, prefix: str, tag: List[str]):
        super().__init__(prefix, tag)

    def mount(self, app: FastAPI):
        app.post(self.generate_route_path(["new-conversation"]), tags=self.tag, response_model=BaseResponse,
                 summary="用户创建新会话")(new_conversation)
        app.post(self.generate_route_path(["llm-chat"]), tags=self.tag, summary="请求LLM聊天接口")(request_llm_chat)
        app.post(self.generate_route_path(["knowledge-base-chat"]), tags=self.tag,
                 summary="请求知识库聊天接口")(request_knowledge_base_chat)
        app.post(self.generate_route_path(["search-engine-chat"]), tags=self.tag,
                 summary="请求搜索引擎聊天接口")(request_search_engine_chat)
        app.post(self.generate_route_path(["online-llm-chat"]), tags=self.tag, summary="请求在线LLM聊天接口")(
            request_online_llm)
        app.post(self.generate_route_path(["mix-chat"]), tags=self.tag, summary="请求混合聊天接口")(request_mix_chat)
        app.post(self.generate_route_path(["stop-llm-chat"]), tags=self.tag, summary="停止LLM聊天接口")(stop_llm_chat)
        app.get(self.generate_route_path(["get-user-conversation"]), tags=self.tag, summary="获取会话列表")(
            get_user_conversations)
        app.get(self.generate_route_path(["get-conversation-record"]), tags=self.tag, summary="获取会话详情")(
            get_conversation_record)
        app.get(self.generate_route_path(["delete-conversation"]),tags=self.tag, summary="删除会话")(delete_user_conversation)
