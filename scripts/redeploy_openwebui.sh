#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${CONTAINER_NAME:-open-webui}"
IMAGE="${IMAGE:-ghcr.io/open-webui/open-webui:ollama}"
HOST_PORT="${HOST_PORT:-3000}"
CONTAINER_PORT="${CONTAINER_PORT:-8080}"
VOL_OPENWEBUI="${VOL_OPENWEBUI:-open-webui}"
VOL_OLLAMA="${VOL_OLLAMA:-ollama}"

docker pull "${IMAGE}"

if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}\$"; then
  docker rm -f "${CONTAINER_NAME}" || true
fi

docker run -d \
  -p "${HOST_PORT}:${CONTAINER_PORT}" \
  -v "${VOL_OLLAMA}":/root/.ollama \
  -v "${VOL_OPENWEBUI}":/app/backend/data \
  --name "${CONTAINER_NAME}" \
  --restart unless-stopped \
  "${IMAGE}"

echo "==============================================="
echo " ✅ Open WebUI redeployed: http://<EC2 IP or DNS>:${HOST_PORT}"
echo "==============================================="
