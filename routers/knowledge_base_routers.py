from typing import List

from fastapi import FastAPI

from message_model.response_model.response import BaseResponse
from routers.mount_routers import routers_mount_interface
from service.knowledge_base_service import create_knowledge_base


class KnowledgeBaseRouters(routers_mount_interface):
    def __init__(self, prefix: str, tag: List[str]):
        super().__init__(prefix, tag)

    def mount(self, app: FastAPI):
        app.post(self.generate_route_path(["create-knowledge-base"]), tags=self.tag, response_model=BaseResponse,
                 summary="用户创建知识库")(create_knowledge_base)
