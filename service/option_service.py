from time import sleep

import requests
from fastapi import Body

from config.llm_config import RELEASE_CONFIG
from message_model.request_model.option_model import changeLLM
from message_model.response_model.response import BaseResponse


def change_llm_model(cl: changeLLM) -> BaseResponse:
    try:
        data = {
            "new_model_name": cl.model_name,
            "keep_origin": RELEASE_CONFIG["keep_origin"]
        }

        response = requests.post(url=RELEASE_CONFIG["url"], json=data)
        sleep(30)
        print(f'切换大模型至{cl.model_name},响应为:{response.text}')
        if "msg" not in response.json():
            return BaseResponse(code=500, msg="切换大模型失败", data={"error": response.text})
        return BaseResponse(code=200, msg="切换大模型成功", data={"msg": response.json()["msg"]})
    except Exception as e:
        return BaseResponse(code=500, msg="切换大模型失败", data={"error": f'{e}'})
