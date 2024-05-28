import jwt
from datetime import datetime, timedelta
import uuid
from config.server_config import JWT_ARGS


def generate_token(email):
    # 载荷包含声明，这里是用户邮箱
    payload = {
        "sub": "user_email",  # 'sub' 代表subject，这里用邮箱标识用户身份
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=1),  # 设置过期时间为1小时后
        "iat": datetime.utcnow(),  # 发行时间
        "jti": str(uuid.uuid4()),  # JWT ID，用于唯一标识JWT，防止重复使用
    }

    # 生成JWT
    token = jwt.encode(payload, JWT_ARGS["secret_key"], algorithm=JWT_ARGS["algorithm"])

    return token
