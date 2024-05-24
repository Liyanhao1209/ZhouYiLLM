from abc import abstractmethod
from typing import List

from fastapi import FastAPI


class routers_mount_interface:

    def __init__(self, prefix: str, tag: List[str]):
        self.prefix = prefix
        self.tag = tag

    @abstractmethod
    def mount(self, app: FastAPI):
        pass


def create_app() -> FastAPI:
    app = FastAPI(title='易学大模型Web应用服务端')
    from routers.sample_router import SampleRouter

    SampleRouter(prefix='/sample', tag=['sample']).mount(app)

    return app
