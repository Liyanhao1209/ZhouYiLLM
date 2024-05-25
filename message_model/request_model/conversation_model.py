from pydantic import BaseModel


class NewConv(BaseModel):
    user_id: str
    conv_name: str | None = "未命名会话"


class LLMChat(BaseModel):
    conv_id: str
    query: str
    prompt_name: str | None = "default"
