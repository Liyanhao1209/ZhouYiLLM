from typing import List

from fastapi import FastAPI

import service.sample_service as sample_service
from routers.mount_routers import routers_mount_interface


class SampleRouter(routers_mount_interface):
    def __init__(self, prefix: str, tag: List[str]):
        super().__init__(prefix, tag)

    def mount(self, app: FastAPI):

        app.get(self.generate_route_path(['say-hello']), tags=self.tag, summary="一个简单的例子")(
            sample_service.hello_world)

        app.get(self.generate_route_path(['say-hello-to-someone', '{username}']), tags=self.tag,
                summary="一个简单的例子")(
            sample_service.specific_id)
