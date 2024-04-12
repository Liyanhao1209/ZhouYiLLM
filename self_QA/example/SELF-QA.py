from zhipuai import ZhipuAI

with open("wenzhang.txt", "r", encoding="UTF-8") as file:
    content = file.read()
    # print(content)
client = ZhipuAI(api_key="")  # 填写您自己的APIKey
messages = [{"role": "user",
             "content": "你是一名研究周易的专家。现在有一篇关于周易的文章，内容为：\n[" + content + "]\n请根据上述文章的内容生成5个关于周易的尽可能专业且多样化的问题。这些问题可以是关于事实的问题，也可以是对相关内容的理解和评价。在提问时，请不要使用“这个”、“那个”等指示代词。\n请按以下格式生成问题:\n1、问题:……\n2. 问题:……"}]
response = client.chat.completions.create(
    model="glm-4",
    messages=messages,
)
print(response.choices[0].message)
messages.append({"role": "assistant",
                 "content": response.choices[0].message.content})
messages.append({"role": "user",
                 "content": "根据文档中的内容，给予每个问题尽可能准确且合乎逻辑的回答。\n请按以下格式生成答案：\n1、回答:……\n2. 回答:……"})
response = client.chat.completions.create(
    model="glm-4",
    messages=messages,
)
print(response.choices[0].message)
