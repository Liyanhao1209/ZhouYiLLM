from pydantic import BaseModel
from sqlalchemy import Text


class BlogModel(BaseModel):
    blog_id: str | None
    title: str
    content: str
    user_id: str
    save_to_kb: bool
