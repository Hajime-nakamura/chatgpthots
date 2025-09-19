#!/usr/bin/env bash
set -euo pipefail

# 初回ビルド＆起動（両サービス）
docker compose up -d --build

echo "==============================================="
echo " ✅ Open WebUI:  http://<EC2 IP or DNS>:3000"
echo " ✅ Flask API :  http://<EC2 IP or DNS>:8000/healthz"
echo "==============================================="
