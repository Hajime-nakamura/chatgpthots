# Open WebUI + Flask Addon (AWS/EC2)

## 概要
- Open WebUI（Ollama 同梱イメージ）と、将来の社内連携・RAG拡張用の最小 Flask API を同時起動する構成。
- `docker-compose.yml` で一発起動。
- AWS EC2 (medium クラス) で GPU なし想定。GPU ありはコメント参照。

## 事前準備
- EC2 セキュリティグループで TCP:3000, 8000 を許可（社内IP/VPN限定推奨）
- EC2 へ Docker / Docker Compose (v2) をインストール

## 初回起動
```bash
cp flask-addon/.env.example flask-addon/.env
chmod +x scripts/*.sh
./scripts/compose_up.sh
