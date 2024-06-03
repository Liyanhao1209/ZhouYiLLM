from typing import List

from fastapi import FastAPI

import service.user_service as user_service
from routers.mount_routers import routers_mount_interface


class UserRouter(routers_mount_interface):
    def __init__(self, prefix: str, tag: List[str]):
        super().__init__(prefix, tag)

    def mount(self, app: FastAPI):
        app.post(self.generate_route_path(["register"]), tags=self.tag, summary="用户注册")(user_service.register_user)
        app.post(self.generate_route_path(["login"]), tags=self.tag, summary="用户登录")(user_service.login_user)
        app.post(self.generate_route_path(["update_info"]), tags=self.tag, summary="更新用户信息")(
            user_service.update_info)
        app.post(self.generate_route_path(["send_verification_code", "{email}"]), tags=self.tag, summary="获取验证码")(
            user_service.send_verification_code)
