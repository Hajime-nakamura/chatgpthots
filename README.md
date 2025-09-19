# Open WebUI + Flask Addon (AWS/EC2)

## 概要
- Open WebUI（Ollama 同梱イメージ）と、将来の社内連携・RAG拡張用の最小 Flask API を同時起動する構成。
- `docker-compose.yml` で一発起動。
- AWS EC2 (medium クラス) で GPU なし想定。GPU ありはコメント参照。

## 事前準備
- EC2 セキュリティグループで TCP:3000, 8000 を許可（社内IP/VPN限定推奨）
- EC2 へ Docker / Docker Compose (v2) をインストール

```bash
sudo apt update -y
sudo apt upgrade -y
# 必要なツール導入
sudo apt install -y ca-certificates curl gnupg lsb-release

# Docker の GPG キー追加
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Docker リポジトリ登録
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# パッケージ更新
sudo apt update -y

# Docker 本体とプラグインをインストール
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
# Docker を起動 & 自動起動有効化
sudo systemctl enable docker
sudo systemctl start docker

# 権限追加（再ログイン後に有効）
sudo usermod -aG docker $USER
newgrp docker
docker --version
docker compose version
```



## 初回起動
```bash
cp flask-addon/.env.example flask-addon/.env
chmod +x scripts/*.sh
./scripts/compose_up.sh
- OLLAMAはyamlに入ってるけど、モデル自体はデプロイされていないので、デプロイしたいモデルを下記でインストール
docker exec -it open-webui ollama pull phi3:3.8b
# 汎用（14B）
docker exec -it open-webui ollama pull phi4:latest

# 数理・推論寄り（14B）
docker exec -it open-webui ollama pull phi4-reasoning:latest

# 軽量版（3.8B）— 日本語＆数学・推論も強化
docker exec -it open-webui ollama pull phi4-mini:latest
