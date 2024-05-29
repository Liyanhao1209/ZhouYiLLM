from zhipuai import ZhipuAI

from config.server_config import ONLINE_LLM_ARGS

zhipu_client = None


def create_zhipu_client():
    global zhipu_client
    zhipu_client = ZhipuAI(api_key=ONLINE_LLM_ARGS["zhipu_api_key"])
    # print("智谱ai客户端加载完成")


def get_zhipu_client():
    global zhipu_client
    if zhipu_client is None:
        create_zhipu_client()
        # print("智谱ai客户端加载完成")
        return zhipu_client
    else:
        return zhipu_client