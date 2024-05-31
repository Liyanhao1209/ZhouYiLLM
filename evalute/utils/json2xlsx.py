import json
import os
import sys
from openpyxl import Workbook


def is_xlsx(file_path: str) -> bool:
    return file_path.endswith('.xlsx')


if __name__ == '__main__':
    args = sys.argv

    path = args[1]
    target = args[2]

    files = os.listdir(path)

    wb = Workbook()

    headers = ["正确答案", "大模型答案"]
    sheets = [wb.active]
    sheets[0].title = f'{files[0]}'
    sheets[0].append(headers)
    for i in range(1, len(files)):
        sheets.append(wb.create_sheet(f'{files[i]}'))
        sheets[i].append(headers)

    for i, fn in enumerate(files):
        with open(os.path.join(path, fn), 'r', encoding='utf-8') as file:
            ans = json.load(file)
        for item in ans:
            sheets[i].append([item['correct_answer'], item['kb_answer']])

    wb.save(target)
