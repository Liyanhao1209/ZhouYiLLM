# 数据集评测脚本
首先需要强调的是，evaluate.py这个脚本已经废弃了，请勿使用

## 层级结构说明
1. config：配置文件，包括评测数据集路径，目标文件路径，请求大模型对话的接口以及实现类对应的参数（例如zhipu glm-4的api_key）
2. interface：请求大模型对话的抽象类以及实现类
3. source：评测数据集
4. target：目标文件

## 使用说明
```commandline
python -m .\evaluate_main_procedure.py
```
1. 如果你想要添加自己的大模型或者是使用额外的可请求的在线大模型进行baseline测试，那么你应该修改：
   1. config/batch_evaluation.json：test_args，配置你的大模型请求对话的参数
   2. interface/impl：添加一个实现类，实现interface/chat_interface.py中的request_chat抽象方法，这个抽象方法应该请求大模型对话并返回一个字典，其中回答的key是"answer"
   3. evaluate_main_procedure.py：在init_model中添加你的实现类到m这个字典中，其中key是你在config/batch_evaluation.json中test_args中配置的key，value是新增大模型实现类的实例
   例如：
   ```json
      ... 其他内容
            "zhipu_ai": {
                "api_key": "you should never know this,my dear friends,use your own api keys",
                "model": "glm-4"
            }
    ```
   随后，
    ```python
    class zhipu_ai(chat_interface):

        def __init__(self, config: json):
            args = config['test_args']['zhipu_ai']
            self.client = ZhipuAI(api_key=args['api_key'])
            self.model = args['model']
    
        def request_chat(self, query: str, config: json) -> Union[dict, json]:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": query
                        }
                    ]
                )
            except Exception as e:
                response = '{\'answer\':\'发生异常' + str(e) + '\'}'
                return response
    
            return {"answer": response.choices[0].message.content}
    ```
    最后，在evaluate_main_procedure.py的init_model中添加你的实现类
   ```python
        # zhipuai:glm-4
       zpa = zhipu_ai(configuration)
       m['zhipu_ai'] = zpa
   ```
2. 如果你想添加新的评测集，请在source文件夹下加入