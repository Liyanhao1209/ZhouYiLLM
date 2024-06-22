# ZhouYiLLM
SDU 2024 项目实训 易学大模型仓库

# 各分支说明
1. main：说明书
2. java_scripts 使用java写成的脚本：
    1. 从非结构化的docx文档（易学百科全书）中提取QA对
    2. 为批处理功能提供实现掉电、宕机容灾机制的工作站
3. python_scripts 使用python写成的脚本：
    1. self-instruct指令生成
    2. self-instruct模板回答
    3. self-qa问答对生成
    4. self-qa prompt模板优化
    5. upload_docs批量上传文件到知识库
    6. evaluate模块基线测试环境评测大模型性能
4. webServer web应用服务端：
    1. component: 类似于Java Spring Bean，容器化机制
    2. config：各类配置文件
    3. db：sqlite建库与数据库表所在地
    4. message_model：消息模型（请求-响应等）
    5. routers：层级路由模型
    6. service：web服务
    7. test：接口测试模块
    8. util：实用工具类
5. webFontEnd web应用客户端
6. interface 第三方重要接口
7. batch_scripts：项目启动批处理脚本


