@echo off
TITLE Start net penetration services

:: 内网穿透服务
echo Starting the zhouyi backend net penetration service...
start npc.exe -server=ihk.fghk.top:8024 -vkey=eec3574f5f

echo Starting the zhouyi frontend net penetration service...
start npc.exe -server=ihk.fghk.top:8024 -vkey=416017f9aa

echo Starting the lc backend net penetration service...
start npc.exe -server=ihk.fghk.top:8024 -vkey=82ec020455