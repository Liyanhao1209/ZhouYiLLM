from abc import abstractmethod, ABC
from typing import List

from fastapi import FastAPI


class routers_mount_interface(ABC):

    def __init__(self, prefix: str, tag: List[str]):
        self.prefix = prefix
        self.tag = tag

    def generate_route_path(self, path: List[str]) -> str:
        if path:
            return f'/{self.prefix}/{"/".join(path)}'

        return f'/{self.prefix}/'

    @abstractmethod
    def mount(self, app: FastAPI):
        pass


def create_app() -> FastAPI:
    app = FastAPI(title='易学大模型Web应用服务端')
    from routers.sample_router import SampleRouter
    from routers.conversation_routers import ConversationRouter
    from routers.administrator_routers import AdministratorRouter

    SampleRouter(prefix='sample', tag=['sample']).mount(app)
    ConversationRouter(prefix='conversation', tag=['conversation management']).mount(app)
    AdministratorRouter(prefix='admin', tag=['admin management']).mount(app)
    return app
