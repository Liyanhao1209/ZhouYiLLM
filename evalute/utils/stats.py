import json
import os
from typing import List

from Baseline_Test_stats.statistic import count_up


def which_is_better(curr: dict, prev: json) -> bool:
    if curr["Solve_rate"] > prev["Solve_rate"]:
        return True
    return False


def absolute_prior_best(dicts: List[dict], llm_model: str, configuration: json) -> bool:
    """
    用来统计明确作答且solve rate最高的数据
    """

    # 打开之前的文件看一下是否结果更好
    stats_result = configuration["target"]
    unresolved_loc = configuration["unresolved_loc"]

    with open(stats_result, "r+", encoding="utf-8") as stats:
        stats_data = json.load(stats)  # 之前的结果

        res, unresolved = count_up(dicts, llm_model)  # res是现在的结果

        for data in stats_data:
            if data["llm_name"] == res["llm_name"] and which_is_better(res, data):
                data["Tot_problem_nums"] = res["Tot_problem_nums"]
                data["Solved_problem_nums"] = res["Solved_problem_nums"]
                data["Solve_rate"] = res["Solve_rate"]
                data["type_stats"] = res["type_stats"]
                # 准备改写 包括json answer,solve_rate，以及unresolved

                # 改写unresolved
                with open(os.path.join(unresolved_loc, f'{llm_model}_unresolved.json'),
                          "w", encoding="utf-8") as unresolved_file:
                    json_str = json.dumps(unresolved_file, ensure_ascii=False, indent=4)
                    unresolved_file.write(json_str)

                stats.seek(0)
                json.dump(stats_data, stats, ensure_ascii=False, indent=4)

                return True
            elif data["llm_name"] == res["llm_name"] and not which_is_better(res, data):
                return False

        # 改写solve_rate
        stats_data.append(res)
        stats.seek(0)
        json.dump(stats_data, stats, ensure_ascii=False, indent=4)
        with open(os.path.join(unresolved_loc, f'{llm_model}_unresolved.json'),
                  "w", encoding="utf-8") as unresolved_file:
            json_str = json.dumps(unresolved, ensure_ascii=False, indent=4)
            unresolved_file.write(json_str)
        return True
