#!/usr/bin/env bash
set -euo pipefail

# Flask サービスのみ再ビルド＆再起動（コード変更時に便利）
docker compose up -d --build flask-addon

echo "==============================================="
echo " ✅ Flask redeployed at http://<EC2 IP or DNS>:8000"
echo "==============================================="
