import json
import os

from evalute.utils.json2xlsx import is_xlsx
from evalute.utils.models import init_models, release_models
from evalute.utils.stats import absolute_prior_best

if __name__ == '__main__':
    with open('./config/batch_evaluate.json', 'r', encoding='utf-8') as cf:
        config = json.load(cf)

    with open('./config/stats_config.json', 'r', encoding='utf-8') as scf:
        stats_config = json.load(scf)

    srcs = config["sources"]
    targets = config["targets"]
    is_prior_best = bool(stats_config["is_prior_best"])

    chats = init_models(config)

    for i in range(len(srcs)):
        src = srcs[i]
        target = targets[i]

        if is_xlsx(src):
            for chat, handlers in chats.items():
                for handler in handlers:
                    model_name = handler.llm_model
                    full_name = f'{chat}_{model_name}'
                    if config["completion"][chat][model_name]:  # 不至于每加一个大模型就把之前跑过的大模型全部重跑一遍，这一块要人工手动维护了
                        continue

                    if model_name in config["test_args"]["release_name"]:  # 需要主动切换模型
                        flag = release_models(config["test_args"]["release_name"][model_name],
                                              config["test_args"]["release_url"])
                        if not flag:
                            continue

                    print(f"{full_name} evaluating {src} ......")

                    ans_key = "text"
                    for ak, mn in config["test_args"]["ans_key"].items():
                        if chat in mn:
                            ans_key = ak
                            break

                    dicts = handler.deal_one_out_of_four_xlsx(src, config, ans_key)

                    if not is_prior_best or is_prior_best and absolute_prior_best(dicts, f'{full_name}', stats_config):
                        with open(os.path.join(target, f"{full_name}.json"), 'w', encoding='utf-8') as tf:
                            json_str = json.dumps(dicts, ensure_ascii=False, indent=4)
                            tf.write(json_str)
                    print(f"{full_name} evaluated {src}")
