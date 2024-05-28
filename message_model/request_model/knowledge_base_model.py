from pydantic import BaseModel


class KnowledgeBase(BaseModel):
    kb_name: str | None
    desc: str | None = "用户并未提供描述"
    user_id: str
