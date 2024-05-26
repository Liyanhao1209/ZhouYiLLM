from pydantic import BaseModel

class RegisterForm(BaseModel):
    email: str
    password: str
