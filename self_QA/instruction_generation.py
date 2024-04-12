import os.path
import random
import re
import sys

import jieba
import pdfplumber
from nltk.translate.bleu_score import SmoothingFunction
from nltk.translate.bleu_score import sentence_bleu
from zhipuai import ZhipuAI


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


# 计算bleu
def calculate_bleu(reference, hypothesis):
    reference_tokens = list(jieba.cut(reference))
    hypothesis_tokens = list(jieba.cut(hypothesis))
    smoothing_function = SmoothingFunction().method7
    score = sentence_bleu([reference_tokens], hypothesis_tokens, smoothing_function=smoothing_function)
    return score


# 将模型的回答转换成问题的列表
def extract_questions(text):
    # 使用正则表达式匹配以数字、空格、英文句号和冒号开头的行
    pattern = r'^\d+\s*[、.]?\s*问题\s*[:：]?\s*(.*)$'
    questions = []

    # 遍历文本的每一行
    for line in text.split('\n'):
        # 使用正则表达式进行匹配
        match = re.match(pattern, line)
        if match:
            question = match.group(1).strip()  # 提取匹配的问题，并去除两端的空格
            questions.append(question)

    return questions


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
            f.write(tasks)


def do_task(task):
    target = open("./self_QA/target/self_QA_instruction.txt", 'r+', encoding="UTF-8")
    instructions = target.readlines()
    sample = random.sample(instructions, 1)

    prompt = "你是一名精通周易的专家，下面是一个与周易相关的问题：\n"
    prompt += "1、问题：" + sample[0] + "\n"
    prompt += "现在给你一段文本，请参考文本内容与上面问题的形式，再提出10个关于周易的比较深入的问题:\n"
    pdf_text = read_pdf(task)
    prompt += pdf_text + "\n"

    global response
    try:
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user",
                 "content": prompt}
            ],
        )
    except Exception as e:
        print(f"发生错误：{e}")

    print(response.choices[0].message.content)

    # 提取问题
    questions = extract_questions(response.choices[0].message.content)
    for i, question in enumerate(questions, start=1):
        print(f"{question}")

    # 指令存储到文件
    for question in questions:
        max_rouge = 0
        for generation_instruction in instructions:
            bleu = calculate_bleu(question, generation_instruction)
            if bleu > max_rouge:
                max_rouge = bleu
        if max_rouge < 0.7:
            print(f"录入：{question}")
            target.write(question + '\n')

    target.close()


if __name__ == '__main__':
    args = sys.argv

    root = args[1]
    client = ZhipuAI(api_key="f283bb78734240c773568def32ec3bcb.T2plYvRz2yltocZT")

    dfs(root)
