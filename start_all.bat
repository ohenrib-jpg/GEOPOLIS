@echo off
echo === GEOPOLIS startup script (Windows) ===
if not exist data\logs mkdir data\logs

echo [1/3] Starting Flask backend...
start "Flask Backend" cmd /c "python backend\core\app.py > data\logs\flask.log 2>&1"

echo [2/3] Waiting for Flask to respond...
setlocal enabledelayedexpansion
for /L %%i in (1,1,30) do (
    curl -s http://localhost:5000/api/status >nul 2>nul
    if !errorlevel! == 0 (
        echo Flask is ready.
        goto startNode
    ) else (
        echo Flask not ready yet... (%%i)
        timeout /t 2 >nul
    )
)
:startNode
echo [3/3] Starting Node.js service...
start "Node Service" cmd /c "node server.js > data\logs\node.log 2>&1"
echo === GEOPOLIS is running ===
echo Flask (port 5000) and Node (port 4000) are active.
echo Logs are stored in data\logs\
