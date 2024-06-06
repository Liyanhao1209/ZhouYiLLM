HOST = '127.0.0.1'

WEB_SERVER = {
    "host": HOST,
    "port": 9090
}

LANGCHAIN_SERVER = {
    # "host": 'zy.tessky.top',
    "host": "127.0.0.1",
    "release": 'release.tessky.top',
    "port": 7861
}

LLM_MODELS = ["yizhou-ft-100", "Qwen-14B-ft-1000", "chatglm3-6b", "yizhou-ft-50", "yizhou-ft-30"]

CHAT_ARGS = {
    "llm_models": LLM_MODELS,
    "history_len": 256,
    "temperature": 0.7,
    "prompt_name": ['default', 'with_history', 'py'],
    "url": f'http://{LANGCHAIN_SERVER["host"]}:{LANGCHAIN_SERVER["port"]}/chat/chat'
    # "url": f'http://{LANGCHAIN_SERVER["host"]}/chat/chat'
}

KB_CHAT_ARGS = {
    "top_k": 5,
    "score_threshold": 1.01,
    "stream": True,
    "url": f'http://{LANGCHAIN_SERVER["host"]}:{LANGCHAIN_SERVER["port"]}/chat/knowledge_base_chat'
    # "url": f'http://{LANGCHAIN_SERVER["host"]}/chat/knowledge_base_chat'
}

SE_CHAT_ARGS = {
    "url": f'http://{LANGCHAIN_SERVER["host"]}:{LANGCHAIN_SERVER["port"]}/chat/search_engine_chat',
    "stream": True,
    # "url": f'http://{LANGCHAIN_SERVER["host"]}/chat/search_engine_chat'
}

ONLINE_LLM_ARGS = {
    "zhipu_api_key": "f283bb78734240c773568def32ec3bcb.T2plYvRz2yltocZT",
    "model": ["glm-4"]
}

EMAIL_ARGS = {
    # 个人邮箱
    "username": 'sdukeji112233@163.com',
    "authorization_code": 'SOKUSUSQOEYZLQPD',
    "host": 'smtp.163.com',
}

REDIS_ARGS = {
    "host": 'localhost',
    "port": 6379,
    "decode_responses": True
}

JWT_ARGS = {
    "secret_key": "SDU_ZhouyiLLM_ljj_lyh_ldl_jfm",
    "algorithm": "HS256",
    "expire_time": 30,
}

CORS_ARGS = {
    "origins": ["*"],
    "credentials": True,
    "methods": ["*"],
    "headers": ["*"]
}
