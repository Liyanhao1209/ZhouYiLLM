import os.path
import sys

import pdfplumber
from docx import Document
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
            f.write(tasks)


def do_task(task):
    text = read_docx(task)
    content = gen_prompt(text)

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

    print(response.choices[0].message.content)


def gen_prompt(text: str) -> str:
    prompt = "你是一名研究周易的专家。现在有一篇关于周易的文章，内容为：\n[" + text + "]\n"
    prompt += ("请根据上述文章的内容生成5"
               "个关于周易的尽可能专业且多样化的问题对（即一个问题及其对应的回答）。这些问答对中的问题可以是关于事实的问题，也可以是对相关内容的理解和评价。在提问时，请不要使用“这个”、“那个”等指示代词。\n")
    prompt += "请按照以下格式生成问题：\n"
    prompt += "1、(问题：......，回答：......)\n1、(问题：......，回答：......)"
    return prompt


if __name__ == '__main__':
    args = sys.argv

    root = args[1]
    client = ZhipuAI(api_key="f283bb78734240c773568def32ec3bcb.T2plYvRz2yltocZT")

    dfs(root)
