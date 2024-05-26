from typing import List

from fastapi import FastAPI

import service.administrator_service as admin_service
from routers.mount_routers import routers_mount_interface


class AdministratorRouter(routers_mount_interface):
    def __init__(self, prefix: str, tag: List[str]):
        super().__init__(prefix, tag)

    def mount(self, app: FastAPI):
        app.get(self.generate_route_path(['see-users-knowledge-base']), tags=self.tag,
                summary="查看用户的知识库")(
            admin_service.see_users_knowledge_base)

        app.get(self.generate_route_path(['see-users-blog', '{user_id}']), tags=self.tag,
                summary="查看用户博客")(
            admin_service.see_users_blog)

        app.post(self.generate_route_path(['add-admin']), tags=self.tag,
                 summary="添加管理员")(
            admin_service.add_administrator)

        app.get(self.generate_route_path(['see_users_record', '{user_id}']), tags=self.tag,
                summary="与大模型的历史会话")(
            admin_service.see_users_record)
