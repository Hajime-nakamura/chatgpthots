#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="open-webui"
IMAGE="ghcr.io/open-webui/open-webui:ollama"
HOST_PORT="3000"
CONTAINER_PORT="8080"
VOL_OPENWEBUI="open-webui"
VOL_OLLAMA="ollama"
PREPULL_MODEL="${PREPULL_MODEL:-llama3.1:8b}"

echo "[INFO] Ensure Docker is installed & running..."
if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com | sh
  sudo systemctl enable docker
  sudo systemctl start docker
fi

docker volume create "${VOL_OPENWEBUI}" >/dev/null
docker volume create "${VOL_OLLAMA}" >/dev/null

if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}\$"; then
  docker rm -f "${CONTAINER_NAME}" || true
fi

docker pull "${IMAGE}"

docker run -d \
  -p "${HOST_PORT}:${CONTAINER_PORT}" \
  -v "${VOL_OLLAMA}":/root/.ollama \
  -v "${VOL_OPENWEBUI}":/app/backend/data \
  --name "${CONTAINER_NAME}" \
  --restart unless-stopped \
  "${IMAGE}"

if [ -n "${PREPULL_MODEL}" ]; then
  echo "[INFO] Pre-pulling model: ${PREPULL_MODEL}"
  docker exec -i "${CONTAINER_NAME}" bash -lc "ollama pull ${PREPULL_MODEL}" || true
fi

echo "==============================================="
echo " ✅ Open WebUI: http://<EC2 IP or DNS>:${HOST_PORT}"
echo "==============================================="
