from typing import List

from fastapi import FastAPI

from routers.mount_routers import routers_mount_interface
from service.conversation_service import new_conversation


class ConversationRouter(routers_mount_interface):
    def __init__(self, prefix: str, tag: List[str]):
        super().__init__(prefix, tag)

    def mount(self, app: FastAPI):
        app.post(self.generate_route_path(["new-conversation"]), tags=self.tag, summary="用户创建新会话")(new_conversation)
