import json
from typing import AsyncIterable

import uvicorn
from aiohttp import ClientSession
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

host = "127.0.0.1"
port = 9090

app = FastAPI(title="sse测试")


async def forward_request_to_kernel(request_body: dict) -> AsyncIterable:
    # 假设这是第三层SSE端点的URL
    third_layer_sse_url = f"http://zy.tessky.top/chat/knowledge_base_chat"

    async with ClientSession() as session:
        async with session.post(third_layer_sse_url, json=request_body) as response:
            if response.status != 200:
                raise Exception(f"Failed to get response from knowledge base: {response.status}")

            # 处理流式响应
            async for chunk in response.content:
                line = chunk.decode()
                if line.startswith("data: "):
                    # 提取data字段后面的内容，并去除尾部的换行符
                    json_data = line[len("data: "):].strip()
                    # 产生JSON数据
                    yield json.loads(json_data)


@app.post("/sse/kb_chat")
async def sse_kb_chat():
    request_body = {
        "query": "如何理解逆向格义？",
        "knowledge_base_name": "faiss_zhouyi",
        "score_threshold": 1.0,
        "top_k": 20,
        "stream": True,
        "model_name": "yizhou-ft-100",
        "temperature": 0.7,
        "prompt_name": "default"
    }

    # async for data in forward_request_to_kernel(request_body):
    #     print(data)

    async def generate_sse():
        async for data in forward_request_to_kernel(request_body):
            event_data = json.dumps(data)
            yield f"data: {event_data}\n\n"

    # 创建 StreamingResponse 对象，并传递生成器
    response = StreamingResponse(generate_sse(), media_type="text/event-stream")

    # 设置必要的头部信息
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"

    return response


if __name__ == '__main__':
    uvicorn.run(app, host=host, port=port)
