import jwt
from datetime import datetime, timedelta
import uuid

# 定义秘钥，用于签名，应妥善保管，不能泄露
SECRET_KEY = "SDU_ZhouyiLLM_ljj_lyh_ldl_jfm"
ALGORITHM = "HS256"  # 使用HS256算法进行签名

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
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token

