#利用glm4选择满足条件的qa对
import json
import os.path
import sys

import pdfplumber
from docx import Document
from rouge import Rouge
from zhipuai import ZhipuAI



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


def update_source_with_extension(source, extension, rouge_l_threshold=0.7):
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
            print(rouge_l)

            if rouge_l['f'] > rouge_l_threshold:
                found_similar = True
                break

        if not found_similar:
            source.append(ext_element)


def qa_pairs_to_json(qa_pairs, existing_data):
    # 将每个问答对转换为{"instruction": ..., "answer": ...}格式
    json_list = [{"instruction": qa["question"], "answer": qa["answer"]} for qa in qa_pairs]

    # 将列表转换为JSON格式的字符串
    update_source_with_extension(existing_data, json_list)
    json_str = json.dumps(existing_data, ensure_ascii=False, indent=2)

    return json_str


def extract_qa_pairs(input_str):
    qa_pairs = []
    # 分割输入字符串为问答对
    pairs = input_str.split("\n\n")

    # 遍历每个问答对
    for i in range(len(pairs)):
        pair = pairs[i]
        # 分割问答对为问题和答案
        lines = pair.strip().split("\n")
        if len(lines) != 2:
            continue
        question = lines[0].strip("问题" + str(i + 1) + ": ")
        answer = lines[1].strip("回答" + str(i + 1) + ": ")

        # 将问答对添加到列表中
        qa_pairs.append({
            "question": question,
            "answer": answer
        })

    return qa_pairs


def gen_prompt(text: str) -> str:
    prompt = "你是一名研究周易的专家。现在有10个关于的周易问答，内容为：\n[" + text + "]\n"
    prompt += ("请从回答的长度和回答的角度从其中满足条件的QA对，都不满足请回答不满足即可。\n"
               "条件如下：\n"
             " 1.回答至少包含三个角度。\n"
             " 2.回答长度大于60个字符。\n"
              "3.回答对问题有详细的解释。\n")
    prompt += "请按照以下格式生成问题与回答：\n"
    prompt += "问题1：......\n回答1：......\n\n问题2：......\n回答2：......"
    return prompt



def do_task(task):
    # text = task
    content = gen_prompt(task)

    print("prompt生成完毕，任务路径：" + task)
    global response
    try:
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user",
                 "content": content}
            ],
        )
    except Exception as e:
        print(f"发生错误：{e}")

#回答
    qa = response.choices[0].message.content
    print(qa)

    qa_pairs = extract_qa_pairs(qa)
    with open('self_qa_correct.json', 'r+', encoding='utf-8') as target_json:
        context = target_json.read()
        print("context:"+context)
        ed = []
        if context:
            target_json.seek(0)
            ed = json.load(target_json)
        qa_json = qa_pairs_to_json(qa_pairs, ed)
        print(qa_json)
        target_json.truncate(0)
        target_json.seek(0)
        target_json.write(qa_json)



#从已有的self_qa.json中循环提取循环问
with open('E:\zhouyi\项目资料\QA-fini\self_qa.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
def judgeQA():
    # 确定列表的长度
    num_records = len(data)

    # 计算需要循环的次数
    num_iterations = num_records // 10 + (1 if num_records % 10 > 0 else 0)
    #计数器

    # 开始循环
    for i in range(num_iterations):
        # 计算每次循环的开始和结束索引
        start_index = i * 10
        end_index = min((i + 1) * 10, num_records)

        # 获取当前批次的记录
        batch = data[start_index:end_index]

        text=''
        count = 0
        # 对当前批次的记录进行处理
        for record in batch:
            count+=1
            # 这里写上你的处理逻辑
            # print(f"处理记录{i} {count}：{record}")

            question = record['instruction']
            answer = record['answer']

            # 将问题和答案格式化为所需的字符串
            formatted_string = f'问题:{question}‘回答’:{answer}'

            # 将格式化后的字符串添加到text中
            text += f"{count}."+formatted_string
        # print(text)
        do_task(text)

if __name__ == '__main__':
    args = sys.argv

    # root = args[1]
    key = args[1]
    client = ZhipuAI(api_key=key)
    judgeQA()
    # dfs(root)
