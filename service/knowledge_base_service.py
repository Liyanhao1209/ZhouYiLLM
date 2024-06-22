import datetime
import uuid
from typing import List, Union

import fastapi.exceptions
import requests
from fastapi import UploadFile, File, Form
from fastapi.responses import FileResponse
from requests import RequestException
from sqlalchemy.orm import Session

import db.create_db
from component.DB_engine import engine
from config.knowledge_base_config import KB_ARGS, DOC_ARGS, FILE_ARGS
from message_model.request_model.knowledge_base_model import KnowledgeBase, DeleteKBFile, DownloadKBFile
from message_model.response_model.response import BaseResponse, ListResponse
from util.utils import request, serialize_knowledge_base


async def create_knowledge_base(kb: KnowledgeBase) -> BaseResponse:
    kb_id = uuid.uuid4().hex
    """
    创建知识库
    1. knowledge_base_name
    2. vector_store_type
    3. embed_model
    """
    request_body = {
        "knowledge_base_name": kb_id,
        "vector_store_type": KB_ARGS["vector_store_type"],
        "embed_model": KB_ARGS["embed_model"],
    }

    response = await request(url=KB_ARGS['url'], request_body=request_body, prefix="")

    if response["success"]:

        try:
            with Session(engine) as session:
                session.add(db.create_db.KnowledgeBase(id=kb_id, name=kb.kb_name, description=kb.desc,
                                                       create_time=datetime.datetime.utcnow(), user_id=kb.user_id))
                session.commit()
        except Exception as e:
            return BaseResponse(code=500, msg="创建知识库失败", data={"error": f'{e}'})

        return BaseResponse(code=200, msg="创建知识库成功", data={"kb_id": kb_id})

    return BaseResponse(code=500, msg="创建知识库失败", data={"error": response["error"]})


async def upload_knowledge_files(
        files: List[UploadFile] = File(..., description="上传文件,支持多文件"),
        kb_id: str = Form(..., description="知识库id")
) -> BaseResponse:
    print(files)
    print(kb_id)
    # 表单参数
    form_data = {
        'knowledge_base_name': kb_id,
        'override': DOC_ARGS["override_custom_docs"],
        'to_vector_store': DOC_ARGS["to_vector_store"],
        'chunk_size': DOC_ARGS["chunk_size"],
        'chunk_overlap': DOC_ARGS["overlap_size"],
        'zh_title_enhance': DOC_ARGS["zh_title_enhance"],
        'docs': DOC_ARGS["docs"],
        'not_refresh_vs_cache': DOC_ARGS["not_refresh_vs_cache"]
    }

    # files = {'files': ("C:\\Users\\Administrator\\Desktop\\upload.txt", open("C:\\Users\\Administrator\\Desktop\\upload.txt", "rb"))}

    files = {'files': (file.filename, file.file) for file in files}

    # print(files)
    # print(form_data)

    try:
        response = requests.post(DOC_ARGS['url'], files=files, data=form_data)
    except Exception as e:
        return BaseResponse(code=500, msg="上传文件失败", data={"error": f'{e}'})

    try:
        if response.ok:
            json_res = response.json()
            print(json_res)
            if json_res["code"] == 200:
                return BaseResponse(code=200, msg="上传文件成功",
                                    data={"failed_files": json_res["data"]["failed_files"]})
            elif json_res["code"] == 404:
                return BaseResponse(code=json_res["code"], msg=json_res["msg"], data=json_res["data"])
    except (fastapi.exceptions.ResponseValidationError, RequestException) as e:
        return BaseResponse(code=200, msg="上传文件成功", data={"failed_files": None, "error": f'{e}'})


async def delete_knowledge_base(kb_id: str) -> BaseResponse:
    try:
        request_body = {
            "knowledge_base_name": kb_id
        }
        response = requests.post(KB_ARGS['delete_url'], headers={"Content-Type": "application/json"}, json=request_body)

        if response.ok:
            json_res = response.json()
            return BaseResponse(code=json_res["code"], msg=json_res["msg"], data={})
    except Exception as e:
        return BaseResponse(code=500, msg="删除知识库失败", data={"error": f'{e}'})


async def delete_knowledge_base_file(dkf: DeleteKBFile):
    try:
        request_body = {
            "knowledge_base_name": dkf.kb_id,
            "file_names": [dkf.file_names]
        }
        response = requests.post(DOC_ARGS['delete_url'], headers={"Content-Type": "application/json"},
                                 json=request_body)

        if response.ok:
            json_res = response.json()
            return BaseResponse(code=json_res["code"], msg=json_res["msg"])
    except Exception as e:
        return BaseResponse(code=500, msg="删除知识库文件失败", data={"error": f'{e}'})


async def download_knowledge_base_file(dkf: DownloadKBFile) -> Union[FileResponse, BaseResponse]:
    try:
        request_body = {
            "knowledge_base_name": dkf.kb_id,
            "file_name": dkf.file_name
        }

        response = requests.post(DOC_ARGS['file_path_url'], headers={"Content-Type": "application/json"},
                                 json=request_body)
        # content_res = requests.get(DOC_ARGS['download_url'], params=request_body)
        # print(response)

        if response.ok:
            # if 'Content-Disposition' in response.headers and 'filename' in response.headers['Content-Disposition']:
            return FileResponse(
                path=response.json()["data"]["filepath"],
                filename=dkf.file_name,
                media_type="multipart/form-data"
            )
            # return BaseResponse(code=200, msg="下载文件成功", data={"content": response.content})
            # else:
            #     # 这不是一个文件，处理 JSON 响应
            #     json_res = response.json()
            #     return BaseResponse(code=json_res.get("code"), msg=json_res.get("msg"), data=json_res.get("data"))
        else:
            # 响应不是 2xx，返回错误 BaseResponse
            return BaseResponse(code=response.status_code, msg="Failed to download file", data={})
    except Exception as e:
        return BaseResponse(code=500, msg="Error while downloading file", data={"error": str(e)})


async def get_user_kbs(user_id: str) -> BaseResponse:
    try:
        with Session(engine) as session:
            user_kbs = session.query(db.create_db.KnowledgeBase).filter(
                db.create_db.KnowledgeBase.user_id == user_id).all()
        return BaseResponse(code=200, msg="获取知识库成功",
                            data={"user_kbs": [serialize_knowledge_base(kb) for kb in user_kbs]})
    except Exception as e:
        return BaseResponse(code=500, msg="获取知识库失败", data={"error": f'{e}'})


async def get_kb_files(kb_id: str) -> Union[BaseResponse, ListResponse]:
    try:
        response = requests.get(FILE_ARGS['url'], params={"knowledge_base_name": kb_id})
        # print(response.json())
        if response.ok:
            return ListResponse(data=response.json()["data"])
    except Exception as e:
        return BaseResponse(code=500, msg="获取知识库文件失败", data={"error": f'{e}'})
