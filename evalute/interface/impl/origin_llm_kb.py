import json
from typing import Union

import requests

from evalute.interface.chat_interface import chat_interface


class origin_llm_kb(chat_interface):

    def request_chat(self, query: str, config: json) -> Union[dict, json]:
        args = config["test_args"]["origin_llm_kb"]

        request_body = {
            "query": query,
            "knowledge_base_name": args["knowledge_base_name"],
            "top_k": args["top_k"],
            "score_threshold": args["score_threshold"],
            "model_name": args["llm_models"][0],
            "temperature": args["temperature"],
            "prompt_name": args["prompt_name"][0],
        }

        try:
            response = requests.post(url=args["url"], headers={"Content-Type": "application/json"}, json=request_body)
        except Exception as e:
            response = '{\'answer\':\'发生异常' + str(e) + '\'}'

        return json.loads(response.text[response.text.find('{'):response.text.rfind('}') + 1])
