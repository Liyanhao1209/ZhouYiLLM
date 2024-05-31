import json
from typing import Union

from zhipuai import ZhipuAI

from evalute.interface.chat_interface import chat_interface


class zhipu_ai(chat_interface):

    def __init__(self, config: json, llm_model: str):
        super().__init__(llm_model)
        args = config['test_args']['zhipu_ai']
        self.client = ZhipuAI(api_key=args['api_key'])
        self.model = args['model']

    def request_chat(self, query: str, config: json) -> Union[dict, json]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            )
        except Exception as e:
            response = '{\'answer\':\'发生异常' + str(e) + '\'}'
            return response

        return {"answer": response.choices[0].message.content}
