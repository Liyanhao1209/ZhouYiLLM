from abc import abstractmethod, ABC
from typing import List
from starlette.middleware.cors import CORSMiddleware
from config.server_config import CORS_ARGS
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
    # 配置跨域
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ARGS["origins"],
        allow_credentials=CORS_ARGS["credentials"],
        allow_methods=CORS_ARGS["methods"],
        allow_headers=CORS_ARGS["headers"],
    )

    from routers.sample_router import SampleRouter
    from routers.conversation_routers import ConversationRouter
    from routers.administrator_routers import AdministratorRouter
    from routers.user_router import UserRouter

    SampleRouter(prefix='sample', tag=['sample']).mount(app)
    ConversationRouter(prefix='conversation', tag=['conversation management']).mount(app)
    AdministratorRouter(prefix='admin', tag=['admin management']).mount(app)
    UserRouter(prefix='user', tag=['user management']).mount(app)


    return app
