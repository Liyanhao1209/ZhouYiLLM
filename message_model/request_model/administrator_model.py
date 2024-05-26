from pydantic import BaseModel


class AdminModel(BaseModel):
    name: str
    password: str


class AdminQueryData(BaseModel):
    id: str
    username: str
    user_id: str
