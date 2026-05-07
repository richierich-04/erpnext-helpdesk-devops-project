#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/home/ubuntu/mygate-it-erp-deploy"
MONITORING_DIR="/home/ubuntu/monitoring"
COMPOSE_FILE="compose.local.yaml"
ENV_FILE="local.env"

echo "========================================"
echo "  ERPNext Staging Deployment"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# --- ERPNext Stack ---
echo "[1/4] Restarting ERPNext containers..."
cd "$APP_DIR"
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d \
  db redis-cache redis-queue backend frontend websocket queue-short queue-long

echo "[2/4] Keeping scheduler disabled (staging safety)..."
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" stop scheduler || true

# --- Monitoring Stack ---
echo "[3/4] Ensuring monitoring stack is up..."
cd "$MONITORING_DIR"
docker compose -f monitoring.compose.yaml up -d --remove-orphans

# --- Health Checks ---
echo "[4/4] Running health checks..."
sleep 10

PASS=0
FAIL=0

check() {
  local name=$1
  local url=$2
  if curl -fsS "$url" >/dev/null 2>&1; then
    echo "  ✓ $name"
    ((PASS++))
  else
    echo "  ✗ $name FAILED"
    ((FAIL++))
  fi
}

check "ERPNext"    "http://localhost:8080"
check "Prometheus" "http://localhost:9090/-/ready"
check "Grafana"    "http://localhost:3000/api/health"

echo ""
echo "Health: $PASS passed, $FAIL failed"

if [ "$FAIL" -gt 0 ]; then
  echo "Deployment completed with failures."
  cd "$APP_DIR"
  docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" ps
  exit 1
fi

echo "========================================"
echo "  Deployment successful ✓"
echo "========================================"
