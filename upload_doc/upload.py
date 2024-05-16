import json
import os
import sys

import pydantic
from typing import Any
from pydantic import BaseModel
import requests


class BaseResponse(BaseModel):
    code: int = pydantic.Field(200, description="API status code")
    msg: str = pydantic.Field("success", description="API status message")
    data: Any = pydantic.Field(None, description="API data")

    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
            }
        }


def do_fail_rec(task):
    with open(failed_root, 'a+', encoding='utf-8') as file:
        file.write(task + '\n')


def request_api(file_path: str, url: str):
    # 准备请求中的文件参数
    with open(file_path, 'rb') as file:
        file = (file_path, file)

    # 其他表单参数
    form_data = {
        'knowledge_base_name': knowledge_base_name,
        'override': override,
        'to_vector_store': to_vector_store,
        'chunk_size': chunk,
        'chunk_overlap': overlap,
        'zh_title_enhance': zh_title_enhance,
        'docs': None,
        'not_refresh_vs_cache': 'False'
    }

    # 发送POST请求
    response = requests.post(url, files={'files': file}, data=form_data)

    # 检查响应
    if response.ok:
        response_data = response.json()
        # 将响应数据转换为BaseResponse对象
        base_response = BaseResponse(**response_data)
        print(
            f"任务{file_path}处理完毕。响应码: {base_response.code}, 响应消息: {base_response.msg}, 数据: {base_response.data}")
    else:
        print(f"任务{file_path}处理失败")
        do_fail_rec(file_path)


if __name__ == '__main__':
    upload_doc_path = sys.argv[1]

    with open(upload_doc_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    fp = config["file_path"]
    failed_root = config["failed_path"]

    split_args = config['split_args']
    chunk = int(split_args['chunk_size'])
    overlap = int(split_args['overlap_size'])
    zh_title_enhance = bool(split_args["zh_title_enhance"])
    knowledge_base_name = split_args["knowledge_base_name"]
    override = bool(split_args["override"])
    to_vector_store = bool(split_args["to_vector_store"])

    for root in fp.values():
        src_paths = root['src_paths']
        api_path = root['api_path']

        for i in range(len(src_paths)):
            for fn in os.listdir(src_paths[i]):
                request_api(os.path.join(src_paths[i], fn), api_path)
