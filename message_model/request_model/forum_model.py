from pydantic import BaseModel


class CommentModel(BaseModel):
    comment: str
    user_id: str
    blog_id: str
