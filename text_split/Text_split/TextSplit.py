import json
import sys
from typing import List
import os
from docx import Document
from textSplitter.chinese_recursive_text_splitter import ChineseRecursiveTextSplitter


def read_docx(docx_path: str) -> str:
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


def do_fail_rec(task):
    with open(failed_root, 'a+', encoding='utf-8') as file:
        file.write(task + '\n')


def do_split(task: str) -> List[str]:
    global chunk, overlap
    try:
        text = read_docx(task)
        # 调分词器
        t_splitter = ChineseRecursiveTextSplitter(
            keep_separator=True,
            is_separator_regex=True,
            chunk_size=chunk,
            chunk_overlap=overlap
        )

        res = t_splitter.split_text(text)
        return res
    except Exception as e:
        print(f'对{task}进行分词时出现错误:{e}')
        do_fail_rec(task)


def do_save(target, res, task, task_name):
    j = 0
    try:
        for j in range(len(res)):
            target_file = os.path.join(target, task_name + f'_split{j}.txt')
            with open(target_file, 'w', encoding='utf-8') as tar:
                tar.write(res[j])
    except Exception as e:
        print(f'保存{task}_{j}时出现错误:{e}')
        do_fail_rec(task)


def dfs_split(path: str, target: str, work_station: str):
    # 获取工作站名称
    ws = os.sep.join([path, work_station])
    # 副本
    ws_tmp = work_station.replace('.txt', '.tmp')
    ws_tmp = os.sep.join([path, ws_tmp])
    # print(f'{ws}\n{ws_tmp}')

    while True:
        with open(ws, 'r+', encoding='utf-8') as file, open(ws_tmp, 'a+', encoding='utf-8') as tmp:
            lines = file.readlines()

            if len(lines) == 0:
                return

            # 读取第一条任务
            task = path + '\\' + lines[0].rstrip()
            # 剩余任务写入副本
            for k in range(1, len(lines)):
                tmp.write(lines[k].rstrip() + '\n')
            print(f'正在处理任务:{task}')

            # 文件夹深搜
            if os.path.isdir(task):
                dfs_split(task, target, work_station)
            else:
                # 分词
                res = do_split(task)
                # 保存
                do_save(target, res, task, lines[0].rstrip())

        if os.path.exists(ws):
            os.remove(ws)
        # 重命名副本覆盖工作站
        os.rename(ws_tmp, ws)


if __name__ == '__main__':
    text_split_path = sys.argv[1]

    with open(text_split_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    fp = config['file_path']
    failed_root = config['failed_path']

    split_args = config['split_args']
    chunk = int(split_args['chunk_size'])
    overlap = int(split_args['overlap_size'])

    for root in fp.values():
        src_paths = root['src_paths']
        target_paths = root['target_paths']
        for i in range(len(src_paths)):
            dfs_split(src_paths[i], target_paths[i], work_station=root['WorkStation'])
