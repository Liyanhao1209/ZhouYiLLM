from config.server_config import LANGCHAIN_SERVER

KB_ARGS = {
    "embed_model": "bge-large-zh-v1.5",
    "vector_store_type": "faiss",
    "url": f'http://{LANGCHAIN_SERVER["address"]}/knowledge_base/create_knowledge_base',
    "delete_url": f'http://{LANGCHAIN_SERVER["address"]}/knowledge_base/delete_knowledge_base',
    "default_kb": "faiss_zhouyi"
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
    "url": f'http://{LANGCHAIN_SERVER["address"]}/knowledge_base/upload_docs',
    "delete_url": f'http://{LANGCHAIN_SERVER["address"]}/knowledge_base/delete_docs',
    "download_url": f'http://{LANGCHAIN_SERVER["address"]}/knowledge_base/download_doc',
    "file_path_url": f'http://{LANGCHAIN_SERVER["address"]}/knowledge_base/get_knowledge_base_file_path'
    # 'url': f'http://{LANGCHAIN_SERVER["host"]}/knowledge_base/upload_docs'
}

FILE_ARGS = {
    "url": f'http://{LANGCHAIN_SERVER["address"]}/knowledge_base/list_files',
    # 'url': f'http://{LANGCHAIN_SERVER["host"]}/knowledge_base/list_files'
    "relative_path": "/static/md/"
}
