@echo off
TITLE Start Services Script

:: Web服务端
echo Activating the first virtual environment and starting the web server...
D:
cd \env\zhouyi_venv\Scripts
call activate
cd D:\longchain\Langchain-Chatchat
start python .\startup.py -a

echo Activating the second virtual environment and starting the web server...
D:
cd D:\zhouyiLLM_code\webServer\.venv\Scripts
call activate
cd D:\zhouyiLLM_code\webServer
start python .\startup.py

:: Web客户端
echo Starting the web client...
cd D:\zhouyiLLM_code\webFrontEnd
start npm run serve

:: Redis for Windows
echo Starting Redis server...
start cmd /c redis-server

:: 等待所有服务启动完成
timeout /t 60 /nobreak
echo All services have been started.

:: 脚本结束
pause