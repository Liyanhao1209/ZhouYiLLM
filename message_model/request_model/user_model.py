from pydantic import BaseModel


class RegisterForm(BaseModel):
    email: str
    password: str
    captcha: str

class LoginForm(BaseModel):
    email: str
    password: str

class InfoForm(BaseModel):
    email: str
    name: str|None
    age: int
    sex: str|None
    description: str|None
