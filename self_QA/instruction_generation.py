import json
import os.path
import sys

import pdfplumber
from docx import Document
from rouge import Rouge
from zhipuai import ZhipuAI


def read_docx(docx_path):
    # 初始化一个Document对象，读取docx文件
    doc = Document(docx_path)

    # 初始化一个空字符串来存储文档中的纯文本
    full_text = []

    # 遍历文档中的每个段落
    for para in doc.paragraphs:
        # 添加段落文本到full_text列表中
        full_text.append(para.text)

        # 将列表中的文本合并成一个字符串并返回
    return '\n'.join(full_text)


def read_pdf(pdf_path):
    text_content = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_content += text + "\n"  # 添加换行符以便区分不同页面的文本
    except Exception as e:
        print(f"读取PDF文件时发生错误: {e}")
        text_content = None

    return text_content


def dfs(path):
    work_station = path + '\\' + 'Workstation.txt'
    with open(work_station, 'r+', encoding='UTF-8') as f:
        tasks = f.readlines()
        while len(tasks) > 0:
            task = path + '\\' + tasks[0].rstrip()
            if os.path.isdir(task):
                dfs(task)
            else:
                do_task(task)
            tasks = tasks[1:]
        f.truncate(0)


def do_task(task):
    text = read_docx(task)
    content = gen_prompt(text)

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

    qa = response.choices[0].message.content
    print(qa)

    qa_pairs = extract_qa_pairs(qa)
    with open('./self_QA/target/self_qa.json', 'r+', encoding='utf-8') as target_json:
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
    prompt = "你是一名研究周易的专家。现在有一篇关于周易的文章，内容为：\n[" + text + "]\n"
    prompt += ("请根据上述文章的内容生成5"
               "个关于周易的尽可能专业且多样化的问题对（即一个问题及其对应的回答）。这些问答对中的问题可以是关于事实的问题，也可以是对相关内容的理解和评价。在提问时，请不要使用“这个”、“那个”等指示代词。\n")
    prompt += "请按照以下格式生成问题与回答：\n"
    prompt += "问题1：......\n回答1：......\n\n问题2：......\n回答2：......"
    return prompt


if __name__ == '__main__':
    args = sys.argv

    root = args[1]
    key = args[2]
    client = ZhipuAI(api_key=key)

    dfs(root)
