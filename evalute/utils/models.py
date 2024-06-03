import json
from collections import defaultdict
from time import sleep
from typing import List

import requests

from evalute.interface.chat_interface import chat_interface
from evalute.interface.impl.kb_chat import kb_chat
from evalute.interface.impl.llm_chat import llm_chat
from evalute.interface.impl.zhipu_ai import zhipu_ai


def init_models(configuration: json) -> dict[str, List[chat_interface]]:
    m = defaultdict(List[chat_interface])

    # 不带知识库
    m["llm_chat"] = [
        llm_chat("chatglm3-6b"),  # 没微调大模型的
        llm_chat("Qwen-14B"),  # 千问大模型
        llm_chat("Qwen-14B-ft-1000")  # 千问微调1000轮
    ]

    # 带知识库
    m["kb_chat"] = [
        kb_chat("chatglm3-6b"),  # glm3-6b没微调
        kb_chat("yizhou-ft-3"),  # glm3-6b微调3轮
        kb_chat("yizhou-ft-30"),  # glm3-6b微调30轮
        kb_chat("yizhou-ft-50"),  # glm3-6b微调50轮
        kb_chat("yizhou-ft-100"),  # glm3-6b微调100轮
        kb_chat("Qwen-14B"),  # 千问大模型
        kb_chat("Qwen-14B-ft-1000")  # 千问1000轮微调
    ]

    m["online_chat"] = [
        zhipu_ai(configuration, "zhipu_ai")
    ]

    return m


def release_models(model_name: str, release_url: str) -> bool:
    try:
        data = {
            "new_model_name": model_name,
            "keep_origin": False
        }
        response = requests.post(url=release_url, json=data)
        sleep(360)  # 异步响应
        print(f'切换大模型至{model_name}的响应为:{response.text}')
        if "msg" not in response.json():
            return False
        return True
    except Exception as e:
        print(f'{e}')
        return False
