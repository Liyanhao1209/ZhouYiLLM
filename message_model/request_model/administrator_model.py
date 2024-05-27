from pydantic import BaseModel


class AdminModel(BaseModel):
    name: str
    password: str


class AdminQueryData(BaseModel):
    id: str | None
    username: str | None
    user_id: str | None
