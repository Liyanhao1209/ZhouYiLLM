import json
import os

from evalute.evaluate import is_xlsx
from evalute.interface.chat_interface import chat_interface
from evalute.interface.impl.origin_llm import origin_llm
from evalute.interface.impl.origin_llm_kb import origin_llm_kb
from evalute.interface.impl.zhipu_ai import zhipu_ai


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

    return m


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

                print(f"{chat} evaluating {src} ......")
                dicts = handler.deal_one_out_of_four_xlsx(src, config, config["test_args"][chat]["ans_key"])
                with open(os.path.join(target, f"{chat}.json"), 'w', encoding='utf-8') as tf:
                    json_str = json.dumps(dicts, ensure_ascii=False, indent=4)
                    tf.write(json_str)
                print(f"{chat} evaluated {src}")
                os.system('cls')
