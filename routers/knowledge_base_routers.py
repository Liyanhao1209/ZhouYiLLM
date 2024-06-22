from typing import List

from fastapi import FastAPI

from message_model.response_model.response import BaseResponse
from routers.mount_routers import routers_mount_interface
from service.knowledge_base_service import create_knowledge_base, upload_knowledge_files, get_user_kbs, get_kb_files, \
    delete_knowledge_base, delete_knowledge_base_file


class KnowledgeBaseRouters(routers_mount_interface):
    def __init__(self, prefix: str, tag: List[str]):
        super().__init__(prefix, tag)

    def mount(self, app: FastAPI):
        app.post(self.generate_route_path(["create-knowledge-base"]), tags=self.tag, response_model=BaseResponse,
                 summary="用户创建知识库")(create_knowledge_base)
        app.post(self.generate_route_path(["upload-knowledge-files"]), tags=self.tag, response_model=BaseResponse,
                 summary="用户上传知识库文件")(upload_knowledge_files)
        app.get(self.generate_route_path(["get-knowledge-base"]), tags=self.tag, response_model=BaseResponse,
                summary="用户获取知识库列表")(get_user_kbs)
        app.get(self.generate_route_path(["get-kb-files"]), tags=self.tag, response_model=BaseResponse,
                summary="用户获取知识库文件列表")(get_kb_files)
        app.post(self.generate_route_path(["delete-knowledge-base"]), tags=self.tag, response_model=BaseResponse,
                 summary="用户删除知识库")(delete_knowledge_base)
        app.post(self.generate_route_path(["delete-knowledge-files"]), tags=self.tag, response_model=BaseResponse,
                 summary="用户删除知识库文件")(delete_knowledge_base_file)
