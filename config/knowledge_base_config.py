from config.server_config import LANGCHAIN_SERVER

KB_ARGS = {
    "embed_model": "bge-large-zh-v1.5",
    "vector_store_type": "faiss",
    "url": f'http://{LANGCHAIN_SERVER["address"]}/knowledge_base/create_knowledge_base'
    # "url": f'http://{LANGCHAIN_SERVER["host"]}/knowledge_base/create_knowledge_base'
}

DOC_ARGS = {
    "override_custom_docs": True,
    "to_vector_store": True,
    "chunk_size": 250,
    "overlap_size": 100,
    "zh_title_enhance": True,
    "not_refresh_vs_cache": False,
    "docs": None,
    "url": f'http://{LANGCHAIN_SERVER["address"]}/knowledge_base/upload_docs'
    # 'url': f'http://{LANGCHAIN_SERVER["host"]}/knowledge_base/upload_docs'
}

FILE_ARGS = {
    "url": f'http://{LANGCHAIN_SERVER["address"]}/knowledge_base/list_files'
    # 'url': f'http://{LANGCHAIN_SERVER["host"]}/knowledge_base/list_files'
}
