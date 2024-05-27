import aioredis

# 使用None初始化，表示初始时未连接
redis = None


async def init_redis_server():
    global redis  # 明确告诉Python我们要修改的是全局的redis变量
    redis = await aioredis.create_redis('redis://127.0.0.1:6379/0')
    print("Redis server initialized.")

# 将redis_set定义为异步函数，并使用await执行Redis操作
def redis_set(email, code):
    if redis is not None:
        redis.set(email, code, ex=60)
    else:
        # await init_redis_server()
        # await redis_set(email, code)
        raise Exception("Redis connection is not initialized.")

def redis_get(key):
    if redis is not None:
        value = redis.get(key)
        return value.decode() if value is not None else None
    else:
        raise Exception("Redis connection is not initialized.")

