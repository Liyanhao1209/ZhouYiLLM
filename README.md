# 易学大模型Web应用服务端文档

## 部署说明
1. 安装Python3.11及以上版本
2. 安装依赖包
```
pip install -r requirements.txt
```
3. 初始化数据库，本项目采用sqlite嵌入式数据库，请运行.\db\create_db.py文件
```
cd -d .\db
python -m create_db.py
```
4. 为了更好的查看sqlite数据库，你可以安装sqlitebrowser，或者是各个IDE中内置的Sqlite插件，或者可以直接下载安装sqlite软件
[sqlite官网](https://www.sqlite.org/)