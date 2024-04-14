import sys

from zhipuai import ZhipuAI
import json

if __name__ == '__main__':
    args = sys.argv
    api_key = args[1]
    with open("self_instruct/target/generation_instruction_part_30001-5009.txt", "r", encoding="UTF-8") as file:
        content = file.readlines()

    file2 = open("self_instruct/target/error_instruction.txt", "a", encoding="UTF-8")
    file3 = open("self_instruct/target/QA_3001-5009.json", "a", encoding="UTF-8")
    index = 0
    while index < len(content):
        instruction = content[index]
        try:
            client = ZhipuAI(api_key=api_key)
            messages = [{"role": "user",
                         "content": f"你是一名研究周易的专家。请给下面的问题给出专业且合理的回答：\n{instruction}"}]
            response = client.chat.completions.create(
                model="glm-4",
                messages=messages,
            )
        except Exception as e:
            print(f"{index+1}   失败   {instruction}")
            print(e)
            file2.write(instruction)
        else:
            answer = response.choices[0].message.content
            QA_dict = {"instruction": instruction, "answer": answer}
            print(f"{index+1}   成功   {QA_dict}")
            file3.write(json.dumps(QA_dict, ensure_ascii=False) + "\n")
        finally:
            index += 1
