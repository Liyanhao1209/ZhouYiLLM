import json
from rouge import Rouge
import sys

def json_to_string(json_obj):
    """将JSON对象转换为字符串"""
    return json.dumps(json_obj, ensure_ascii=False, sort_keys=True)
def compute_rouge_l_score(reference, summary):
    """
    计算ROUGE-L分数

    参数:
    reference (str): 参考文本。
    summary (str): 摘要文本。

    返回:
    dict: 包含ROUGE-L分数的字典，包括precision, recall, 和fmeasure。
    """
    rouge = Rouge()
    scores = rouge.get_scores(summary, reference, avg=True)
    return scores['rouge-l']


def update_source_with_extension(source, extension,output_file, rouge_l_threshold=0.7):
    """
    根据ROUGE-L分数更新source列表，将extension中与source中元素不相似（ROUGE-L分数不大于阈值）的元素添加到source中。

    参数:
        source (list): 原始的JSON对象列表。
        extension (list): 要添加的JSON对象列表。
        rouge_l_threshold (float): ROUGE-L分数的阈值，用于决定是否添加元素。

    返回:
        None (直接修改传入的source列表)
    """
    for ext_element in extension:
        ext_str = json_to_string(ext_element)
        found_similar = False

        for src_element in source:
            src_str = json_to_string(src_element)
            rouge_l = compute_rouge_l_score(src_str, ext_str)
            # print(rouge_l)

            if rouge_l['f'] > rouge_l_threshold:
                found_similar = True
                break

        if not found_similar:
            source.append(ext_element)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(source, f, ensure_ascii=False, indent=4)



if __name__ == '__main__':
    args = sys.argv

    src_file = args[1]
    target_file = args[2]
    output_file = args[3]

    with open(src_file, 'r', encoding='utf-8') as src_json:
        src_lists = json.load(src_json)
    with open(target_file, 'r', encoding='utf-8') as target_json:
        target_lists = json.load(target_json)

    update_source_with_extension(src_lists, target_lists,output_file)
