from typing import List

from fastapi import FastAPI

import service.blog_service as blog_service
from routers.mount_routers import routers_mount_interface


class BlogRouter(routers_mount_interface):
    def __init__(self, prefix: str, tag: List[str]):
        super().__init__(prefix, tag)

    def mount(self, app: FastAPI):
        app.post(self.generate_route_path(['add_blog']), tags=self.tag,
                 summary="添加博客")(
            blog_service.add_blog)
        app.get(self.generate_route_path(['get_blog_list', '{user_id}']), tags=self.tag,
                summary="获取列表")(
            blog_service.get_blog)
        app.get(self.generate_route_path(['delete', '{blog_id}']), tags=self.tag,
                summary="删除博客")(
            blog_service.delete_blog)
