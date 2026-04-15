#!/bin/bash
# ==========================================
# Local Docker Development Deployment
# ==========================================
# This script is for LOCAL development only.
# It uses docker-compose.yml with volume mounts.
# Database and migrations are isolated to your local machine.
# ==========================================

set -e

echo "=========================================="
echo "LOCAL DOCKER DEPLOYMENT"
echo "=========================================="
echo ""
echo "This will:"
echo "  - Build local dev containers"
echo "  - Create/migrate local dev database"
echo "  - Create local superuser for testing"
echo "  - Start containers with hot-reload"
echo ""
echo "Press CTRL+C to cancel, or wait 3 seconds to continue..."
sleep 3

echo ""
echo "[1/7] Stopping existing containers..."
docker compose -f docker-compose.yml down --remove-orphans
docker compose -f docker-compose.yml rm -f 2>/dev/null || true

# remove all volumes
docker compose -f docker-compose.yml down -v --remove-orphans
docker system prune -a -f

echo ""
echo "[2/7] Building dev containers..."
docker compose -f docker-compose.yml build



echo "Waiting for database to become healthy..."
for i in {1..30}; do
  # check db from the database host not on docker container
  if pg_isready -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USER} -d ${DB_NAME}; then
    echo "Database is healthy."
    break
  fi
  if [ "$i" -eq 30 ]; then
    echo "Database did not become healthy in time."
    exit 1
  fi
  sleep 2
done


echo ""
echo "[5.5/7] Making migrations..."
docker compose -f docker-compose.yml run --rm web python manage.py makemigrations

echo ""
echo "[5/7] Running migrations..."
docker compose -f docker-compose.yml run --rm web python manage.py migrate --noinput


echo ""
echo "[7/7] Collecting static files..."
docker compose -f docker-compose.yml run --rm web python manage.py collectstatic --noinput

echo ""
echo "[post-deploy] Seeding all data (admin user + config + app data)..."
docker compose -f docker-compose.yml run --rm web python manage.py create_user || echo "User creation step failed (non-fatal)"

echo ""
echo "=========================================="
echo "Starting local development server..."
echo "=========================================="
docker compose -f docker-compose.yml up -d

echo ""
echo "=========================================="
echo "LOCAL DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "Services:"
echo "  - API: http://localhost:${WEB_PORT:-9001}"
echo "  - Admin: http://localhost:${WEB_PORT:-9001}/admin"
echo "  - Credentials: admin / helpo"
echo ""
echo "View logs:  make dev-logs"
echo "Stop:       make dev-down"
echo ""
