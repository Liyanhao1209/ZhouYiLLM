import json
import os
from time import sleep

import requests

from evalute.evaluate import is_xlsx
from evalute.interface.chat_interface import chat_interface
from evalute.interface.impl.origin_llm import origin_llm
from evalute.interface.impl.origin_llm_kb import origin_llm_kb
from evalute.interface.impl.zhipu_ai import zhipu_ai
from evalute.interface.impl.zhouyi_ft import zhouyi_ft


def init_models(configuration: json) -> dict[str, chat_interface]:
    m = {}

    # ours:不带知识库且不带微调大模型的
    ol = origin_llm()
    m['origin_llm'] = ol
    # ours:带知识库但是不带微调大模型的
    olk = origin_llm_kb()
    m['origin_llm_kb'] = olk
    # zhipuai:glm-4
    zpa = zhipu_ai(configuration)
    m['zhipu_ai'] = zpa
    # ft-100 微调100轮的
    ft_100 = zhouyi_ft(0)
    m['yizhou-ft-100'] = ft_100
    # ft-50 微调50轮的
    ft_50 = zhouyi_ft(1)
    m['yizhou-ft-50'] = ft_50
    # ft-30 微调30轮的
    ft_30 = zhouyi_ft(2)
    m['yizhou-ft-30'] = ft_30
    # ft-30 微调3轮的
    ft_3 = zhouyi_ft(3)
    m['yizhou-ft-3'] = ft_3
    # ft-100-kb 微调100轮带知识库
    ft_100_kb = zhouyi_ft(0)
    m['yizhou-ft-100-kb'] = ft_100_kb
    # ft-50-kb 微调50轮带知识库
    ft_50_kb = zhouyi_ft(1)
    m['yizhou-ft-50-kb'] = ft_50_kb
    # ft-30-kb 微调30轮带知识库
    ft_30_kb = zhouyi_ft(2)
    m['yizhou-ft-30-kb'] = ft_30_kb
    # ft-3-kb 微调3轮带知识库
    ft_3_kb = zhouyi_ft(3)
    m['yizhou-ft-3-kb'] = ft_3_kb
    return m


def release_models(model_name: str, configuration: json) -> bool:
    try:
        data = {
            "new_model_name": model_name,
            "keep_origin": False
        }
        response = requests.post(url=configuration["test_args"]["release_url"], json=data)
        sleep(30)  # 异步响应
        print(f'切换大模型至{model_name}的响应为:{response.text}')
        if "msg" not in response.json():
            return False
        return True
    except Exception as e:
        print(f'{e}')
        return False


if __name__ == '__main__':
    with open('./config/batch_evaluate.json', 'r', encoding='utf-8') as cf:
        config = json.load(cf)

    srcs = config["sources"]
    targets = config["targets"]

    chats = init_models(config)

    for i in range(len(srcs)):
        src = srcs[i]
        target = targets[i]

        if is_xlsx(src):
            for chat, handler in chats.items():
                if config["completion"][chat]:  # 不至于每加一个大模型就把之前跑过的大模型全部重跑一遍，这一块要人工手动维护了
                    continue

                if chat in config["test_args"]["release_name"]:  # 需要主动切换模型
                    flag = release_models(config["test_args"]["release_name"][chat], config)
                    if not flag:
                        continue

                print(f"{chat} evaluating {src} ......")

                ans_key = "text"
                for ak, mn in config["test_args"]["ans_key"].items():
                    if chat == mn:
                        ans_key = ak
                        break

                dicts = handler.deal_one_out_of_four_xlsx(src, config, ans_key)
                with open(os.path.join(target, f"{chat}.json"), 'w', encoding='utf-8') as tf:
                    json_str = json.dumps(dicts, ensure_ascii=False, indent=4)
                    tf.write(json_str)
                print(f"{chat} evaluated {src}")
                os.system('cls')
