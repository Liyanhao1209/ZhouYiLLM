from typing import List

from fastapi import UploadFile
from pydantic import BaseModel


class KnowledgeBase(BaseModel):
    kb_name: str | None
    desc: str | None = "用户并未提供描述"
    user_id: str


class KBFile(BaseModel):
    files: List[UploadFile]
    knowledge_base_id: str


class DeleteKB(BaseModel):
    kb_id: str


class DeleteKBFile(BaseModel):
    kb_id: str
    file_names: str
