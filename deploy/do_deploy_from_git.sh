#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/cgallego17/mana-optical.git"
BRANCH="main"

BASE_DIR="/var/www/mana"
REPO_DIR="$BASE_DIR/repo"
BACKEND_TARGET="$BASE_DIR/backend"
WEB_TARGET="$BASE_DIR/web"
BACKEND_ENV="$BACKEND_TARGET/.env"
ENV_BACKUP="$BASE_DIR/.env.backend.bak"
BACKEND_DB="$BACKEND_TARGET/db.sqlite3"
DB_BACKUP="$BASE_DIR/db.sqlite3.bak"

if [[ $EUID -ne 0 ]]; then
  echo "Run as root (sudo)" >&2
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive

# Ensure deps exist
command -v git >/dev/null 2>&1 || (apt-get update && apt-get install -y git)
command -v node >/dev/null 2>&1 || (apt-get update && apt-get install -y nodejs npm)

NODE_MAJOR="$(node -v 2>/dev/null | tr -d 'v' | cut -d. -f1 || echo 0)"
if [[ "$NODE_MAJOR" -lt 20 ]]; then
  apt-get update
  apt-get install -y curl ca-certificates
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
  apt-get install -y nodejs
fi

# Mitigate low-memory droplets (e.g. 512MB): add swap if none exists
if ! swapon --show | grep -q '^/'; then
  if [[ ! -f /swapfile ]]; then
    fallocate -l 2G /swapfile || dd if=/dev/zero of=/swapfile bs=1M count=2048
    chmod 600 /swapfile
    mkswap /swapfile
  fi
  swapon /swapfile || true
fi

mkdir -p "$BASE_DIR"

if [[ -d "$REPO_DIR/.git" ]]; then
  echo "Updating repo..."
  git config --global --add safe.directory "$REPO_DIR" >/dev/null 2>&1 || true
  git -C "$REPO_DIR" fetch --all
  git -C "$REPO_DIR" checkout "$BRANCH"
  git -C "$REPO_DIR" pull --ff-only
else
  echo "Cloning repo..."
  git clone --branch "$BRANCH" "$REPO_URL" "$REPO_DIR"
fi

# Build frontend
if [[ ! -f "$REPO_DIR/web/package.json" ]]; then
  echo "web/package.json not found in repo" >&2
  exit 1
fi

echo "Building frontend..."
( 
  cd "$REPO_DIR/web"
  npm ci
  MEM_MB="$(awk '/MemTotal/ {print int($2/1024)}' /proc/meminfo 2>/dev/null || echo 0)"
  if [[ "$MEM_MB" -gt 0 && "$MEM_MB" -lt 900 ]]; then
    echo "Low RAM detected (${MEM_MB}MB). Running 'vite build' only (skipping vue-tsc)."
    NODE_OPTIONS="--max-old-space-size=2048" npx vite build
  else
    NODE_OPTIONS="--max-old-space-size=2048" npm run build
  fi
)

# Preserve backend env + base de datos entre deploys (backend folder is
# replaced). db.sqlite3 está en .gitignore, así que NUNCA existe dentro del
# checkout del repo: sin este backup/restore, cada "rm -rf backend" borraba
# la base de datos de producción entera y "migrate" la recreaba vacía.
if [[ -f "$BACKEND_ENV" ]]; then
  cp -f "$BACKEND_ENV" "$ENV_BACKUP"
fi
if [[ -f "$BACKEND_DB" ]]; then
  cp -f "$BACKEND_DB" "$DB_BACKUP"
fi

# Detener gunicorn antes de tocar el directorio del backend: si un worker
# se reinicia (timeout, falta de RAM) justo mientras rm -rf/cp -R lo dejan
# vacío o a medio copiar, revienta con ImportError al re-importar el código.
systemctl stop mana-backend 2>/dev/null || true

# Sync backend + deploy files
echo "Syncing backend..."
rm -rf "$BACKEND_TARGET"
cp -R "$REPO_DIR/backend" "$BACKEND_TARGET"

if [[ -f "$ENV_BACKUP" && ! -f "$BACKEND_ENV" ]]; then
  cp -f "$ENV_BACKUP" "$BACKEND_ENV"
fi
if [[ -f "$DB_BACKUP" && ! -f "$BACKEND_DB" ]]; then
  cp -f "$DB_BACKUP" "$BACKEND_DB"
fi

echo "Syncing web dist..."
mkdir -p "$WEB_TARGET"
rm -rf "$WEB_TARGET/dist"
cp -R "$REPO_DIR/web/dist" "$WEB_TARGET/dist"
chown -R www-data:www-data "$WEB_TARGET"

echo "Syncing deploy scripts..."
rm -rf "$BASE_DIR/deploy"
cp -R "$REPO_DIR/deploy" "$BASE_DIR/deploy"

if [[ ! -f "$BACKEND_TARGET/.env" ]]; then
  echo "Missing $BACKEND_TARGET/.env" >&2
  echo "Create it from $BASE_DIR/deploy/env.example" >&2
  exit 1
fi

echo "Running deploy..."
bash "$BASE_DIR/deploy/do_deploy.sh"

echo "Done."
