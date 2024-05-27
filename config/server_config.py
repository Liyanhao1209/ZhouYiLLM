HOST = '127.0.0.1'

WEB_SERVER = {
    "host": HOST,
    "port": 9090
}

LANGCHAIN_SERVER = {
    "host": '121.250.210.123',
    "port": 7861
}

LLM_MODELS = ["chatglm3-6b", "zhipu-api", "openai-api"]

CHAT_ARGS = {
    "llm_models": LLM_MODELS,
    "history_len": 256,
    "temperature": 0.7,
    "prompt_name": ['default', 'with_history', 'py'],
    "url": f'http://{LANGCHAIN_SERVER["host"]}:{LANGCHAIN_SERVER["port"]}/chat/chat'
}

KB_CHAT_ARGS = {
    "top_k": 20,
    "score_threshold": 1.01,
    "url": f'http://{LANGCHAIN_SERVER["host"]}:{LANGCHAIN_SERVER["port"]}/chat/knowledge_base_chat'
}

SE_CHAT_ARGS = {
    "url": f'http://{LANGCHAIN_SERVER["host"]}:{LANGCHAIN_SERVER["port"]}/chat/search_engine_chat'
}

EMAIL_ARGS = {
    # 个人邮箱
    "username": 'sdukeji112233@163.com',
    "authorization_code": 'SOKUSUSQOEYZLQPD',
    "host": 'smtp.163.com',
}


