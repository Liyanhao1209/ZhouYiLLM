import json

import requests


async def request(url: str, request_body: dict, prefix: str) -> dict:
    try:
        response = requests.post(url=url, headers={"Content-Type": "application/json"}, json=request_body)
        # print(response.text)
        text = response.text[response.text.find('{'):response.text.rfind('}') + 1]
        print(text)
    except Exception as e:
        return {"success": False, "error": f'{e}'}

    if response.ok:
        return {"success": True, "data": json.loads(text)}

    return {"success": False, "error": f'{response.text}'}
