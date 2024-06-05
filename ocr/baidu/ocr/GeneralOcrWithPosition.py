import base64
import json
import os
from time import sleep

import pdfplumber
import requests


def get_tot_pages(file_path: str) -> int:
    with pdfplumber.open(file_path) as pdf:
        return len(pdf.pages)


def ocr(file_path: str, auth_config: json, ocr_config: json) -> dict:
    req_url = ocr_config["request_url"]
    access_token = auth_config["access_token"]

    url = f'{req_url}?access_token={access_token}'
    headers = ocr_config["headers"]

    file = open(file_path, 'rb')
    pdf = base64.b64encode(file.read())

    m = {}
    for i in range(1, get_tot_pages(file_path) + 1):
        sleep(2)
        print(f'正在处理{file_path}的第{i}页...')
        params = {"pdf_file": pdf, "pdf_file_num": i}
        response = requests.post(url, data=params, headers=headers)
        if response:
            res_json = response.json()
            print(f'处理结果:{res_json}')
            if "words_result" in res_json:
                m[f'page{i}'] = res_json["words_result"]
                print(f'处理{file_path}的第{i}页完毕')

    return m


if __name__ == '__main__':
    with open('../config/auth_config.json', 'r', encoding='utf-8') as acf:
        ac = json.load(acf)

    with open('../config/ocr_config.json', 'r', encoding='utf-8') as ocf:
        oc = json.load(ocf)

    for dir_path, dir_names, filenames in os.walk(oc["src_root"]):
        for fn in filenames:
            p = os.path.join(dir_path, fn)
            res = ocr(str(p), ac, oc)
            with open(os.path.join(oc["target_root"], fn.replace('.pdf', '.json')), 'w', encoding='utf-8') as f:
                json.dump(res, f, ensure_ascii=False, indent=4)
