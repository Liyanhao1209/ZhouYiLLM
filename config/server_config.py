HOST = '127.0.0.1'

WEB_SERVER = {
    "host": HOST,
    "port": 9090
}

LANGCHAIN_SERVER = {
    "host": '121.250.210.123',
    "port": 7861
}

CHAT_ARGS = {
    "llm_models": ["chatglm3-6b", "zhipu-api", "openai-api"],
    "history_len": 256,
    "temperature": 0.7,
    "prompt_name": ['default', 'with_history', 'py'],
    "url": f'http://{LANGCHAIN_SERVER["host"]}:{LANGCHAIN_SERVER["port"]}/chat/chat'
}
