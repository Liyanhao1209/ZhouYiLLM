from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from component.DB_engine import engine
from db.create_db import User
from config.server_config import JWT_ARGS

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 生成token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_ARGS["secret_key"], algorithm=JWT_ARGS["algorithm"])
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    print(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_ARGS["secret_key"], algorithms=[JWT_ARGS["algorithm"]])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        # token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    with Session(engine) as session:
        user = session.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
