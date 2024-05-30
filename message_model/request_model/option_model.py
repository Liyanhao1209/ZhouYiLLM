from pydantic import BaseModel


class changeLLM(BaseModel):
    model_name: str | None = "chatglm3-6b"
