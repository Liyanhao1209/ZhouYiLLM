from typing import List

from fastapi import FastAPI

import service.forum_service as forum_service
from routers.mount_routers import routers_mount_interface


class ForumRouter(routers_mount_interface):
    def __init__(self, prefix: str, tag: List[str]):
        super().__init__(prefix, tag)

    def mount(self, app: FastAPI):
        app.get(self.generate_route_path(['get_all_blogs', '{login_user_id}']), tags=self.tag,
                summary="获取博客")(
            forum_service.get_all_blogs)
        app.post(self.generate_route_path(['add_comment']), tags=self.tag,
                 summary="评论")(
            forum_service.add_comment)
        app.get(self.generate_route_path(['get_comment', '{blog_id}']), tags=self.tag,
                summary="获取博客的评论")(
            forum_service.get_comment)
        app.post(self.generate_route_path(['delete_comment', '{comment_id}', '{blog_id}', '{user_id}']), tags=self.tag,
                 summary="删除评论")(
            forum_service.delete_comment)
        app.post(self.generate_route_path(['star_unstar_blog', '{user_id}', '{blog_id}']), tags=self.tag,
                 summary="收藏/取消收藏")(
            forum_service.star_unstar_blog)
        app.get(self.generate_route_path(['get_star_blog', '{user_id}']), tags=self.tag,
                summary="获取收藏博客")(
            forum_service.get_star_blog)
