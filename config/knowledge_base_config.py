from config.server_config import LANGCHAIN_SERVER

KB_ARGS = {
    "embed_model": "bge-large-zh-v1.5",
    "vector_store_type": "faiss",
    "url": f'http://{LANGCHAIN_SERVER["host"]}/knowledge_base/create_knowledge_base'
}
