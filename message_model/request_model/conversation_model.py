from pydantic import BaseModel


class NewConv(BaseModel):
    user_id: str
    conv_name: str | None = "未命名会话"
