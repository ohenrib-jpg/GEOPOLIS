#!/bin/bash
echo "=== GEOPOLIS startup script (Linux/Render) ==="
mkdir -p data/logs

echo "[1/3] Starting Flask backend..."
nohup python3 backend/core/app.py > data/logs/flask.log 2>&1 &
FLASK_PID=$!
echo "Flask PID: $FLASK_PID"

echo "[2/3] Waiting for Flask to respond..."
for i in {1..30}
do
    if curl -s http://localhost:5000/api/status > /dev/null; then
        echo "Flask is ready."
        break
    else
        echo "Flask not ready yet... ($i)"
        sleep 2
    fi
done

echo "[3/3] Starting Node.js service..."
nohup node server.js > data/logs/node.log 2>&1 &
NODE_PID=$!
echo "Node PID: $NODE_PID"

echo "=== GEOPOLIS is running ==="
echo "Flask (port 5000) and Node (port 4000) are active."
echo "Logs: data/logs/flask.log and data/logs/node.log"
