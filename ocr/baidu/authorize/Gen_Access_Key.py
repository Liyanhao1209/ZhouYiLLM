import json

import requests


# 获取AK技术文档：https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu

def gen_ak():
    with open('../config/auth_config.json', 'r+', encoding='utf-8') as acf:
        config = json.load(acf)

        api_key = config['API_Key']
        secret_key = config['Secret_Key']
        token_url = 'https://aip.baidubce.com/oauth/2.0/token'

        url = f'{token_url}?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}'
        payload = ""

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        res_json = response.json()

        if "error" not in res_json:
            acf.seek(0)
            config['access_token'] = res_json['access_token']
            config['expires_in'] = res_json['expires_in']
            json.dump(config, acf, indent=4, ensure_ascii=False)
        else:
            print(f'请求失败:{response.text}')


if __name__ == '__main__':
    gen_ak()
