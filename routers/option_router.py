from typing import List

from fastapi import FastAPI

from message_model.response_model.response import BaseResponse
from routers.mount_routers import routers_mount_interface
from service.option_service import change_llm_model


class OptionRouter(routers_mount_interface):
    def __init__(self, prefix: str, tag: List[str]):
        super().__init__(prefix, tag)

    def mount(self, app: FastAPI):
        app.post(self.generate_route_path(['change-llm-model']), tags=self.tag, summary="更换大语言模型",
                 response_model=BaseResponse)(
            change_llm_model
        )