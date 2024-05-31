import json
from typing import Union

import requests

from evalute.interface.chat_interface import chat_interface


class llm_chat(chat_interface):

    def __init__(self, llm_model: str):
        super().__init__(llm_model)

    def request_chat(self, query: str, config: json) -> Union[dict, json]:
        args = config["test_args"]["llm_chat"]

        request_body = {
            "query": query,
            "history_len": args["history_len"],
            "model_name": self.llm_model,
            "temperature": args["temperature"],
            "prompt_name": args["prompt_name"][0],
        }

        try:
            response = requests.post(url=args["url"], headers={"Content-Type": "application/json"}, json=request_body)
        except Exception as e:
            response = '{\'answer\':\'发生异常' + str(e) + '\'}'

        return json.loads(response.text[response.text.find('{'):response.text.rfind('}') + 1])
