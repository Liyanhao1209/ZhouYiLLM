from config.server_config import LANGCHAIN_SERVER

RELEASE_CONFIG = {
    "keep_origin": False,
    "url": f'http://{LANGCHAIN_SERVER["release"]}/release'
}
