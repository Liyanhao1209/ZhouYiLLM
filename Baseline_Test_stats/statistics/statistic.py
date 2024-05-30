import json

"""
现在的需求是，统计这个json数组一共有多少json对象，统计这些json对象中，correct_answer和kb_answer能够对应的有多少？
统计后者与前者的比值，保留四位小数。
作为一个json对象返回，包括四个kv对，
Tot_problem_nums,
Solved_problem_nums,
Solve_rate,
llm_name

子任务2：现在有多个子任务1，使用json文件对其进行配置：
包括子任务1中提到的json文件的路径以及目标文件路径。
对多个json文件调用子任务1的过程，得到一个json数组，写入配置的目标文件中。
测试与开发环境在仓库的python_scripts分支下的evaluate模块。
新增子模块Baseline_Test_Stats，在子模块下完成这两个子任务。入参的json文件我提供
"""


def count_up(jsons, llm_name):
    total_num = len(jsons)
    solved_num = 0
    for j in jsons:
        correct_answer = str(j['correct_answer'])
        kb_answer = str(j['kb_answer'])
        if kb_answer.find(correct_answer) > 0:
            solved_num += 1
    rate = format(solved_num / total_num, '.4f')
    return {
        "Tot_problem_nums": total_num,
        "Solved_problem_nums": solved_num,
        "Solve_rate": rate,
        "llm_name": llm_name
    }


if __name__ == '__main__':
    with open('config/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    files = config['source']
    base = config['base_loc']
    target = config['target']
    res = []
    for name in files:
        loc = base + name + '.json'
        with open(loc, 'r', encoding='utf-8') as cf:
            jsonlist = json.load(cf)
        res.append(count_up(jsonlist, name))
    with open(target, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)
    print('done')

