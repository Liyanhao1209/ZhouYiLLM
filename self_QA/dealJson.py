#完善json qa对的格式
import json
# 原始列表
with open('self_qa_correct.json', 'r', encoding='utf-8') as file:
    lists = json.load(file)

# 过滤和清理列表
filtered_list = []
for item in lists:
    if "不满足条件" not in item["answer"]:
        # 删除 "instruction" 和 "answer" 的前面的 "：" 和数字
        new_instruction = item["instruction"].lstrip("：0123456789")
        new_answer = item["answer"].lstrip("：0123456789")
        filtered_list.append({"instruction": new_instruction, "answer": new_answer})

# for item in filtered_list:
#     print(item)

with open('self_qa_correct.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_list, f, ensure_ascii=False, indent=4)

# with open('self_qa_correct.json', 'r+', encoding='utf-8') as target_json:
#     target_json.write(qa_json)
