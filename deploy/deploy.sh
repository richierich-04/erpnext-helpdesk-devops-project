#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/home/ubuntu/mygate-it-erp-deploy"
COMPOSE_FILE="compose.local.yaml"
ENV_FILE="local.env"

echo "Starting ERPNext Helpdesk staging deployment..."
cd "$APP_DIR"

echo "Current containers:"
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" ps

echo "Pulling latest images if available..."
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" pull || true

echo "Restarting application containers..."
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d \
  db redis-cache redis-queue backend frontend websocket queue-short queue-long

echo "Keeping scheduler disabled for staging safety..."
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" stop scheduler || true

echo "Running health check..."
sleep 10

if curl -fsS http://localhost:8080 >/dev/null; then
  echo "Health check passed: ERPNext Helpdesk is reachable on localhost:8080"
else
  echo "Health check failed"
  docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" ps
  exit 1
fi

echo "Deployment complete."
