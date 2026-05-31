#!/usr/bin/env bash
set -euo pipefail

APP_NAME="mana"
BASE_DIR="/var/www/mana"
BACKEND_DIR="$BASE_DIR/backend"
WEB_DIR="$BASE_DIR/web"

if [[ $EUID -ne 0 ]]; then
  echo "Run as root (sudo)" >&2
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y \
  python3 python3-venv python3-pip \
  git \
  nginx \
  nodejs npm \
  ufw \
  curl

NODE_MAJOR="$(node -v 2>/dev/null | tr -d 'v' | cut -d. -f1 || echo 0)"
if [[ "$NODE_MAJOR" -lt 20 ]]; then
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
  apt-get install -y nodejs
fi

mkdir -p "$BACKEND_DIR" "$WEB_DIR"

# Create system user/group if missing
if ! id -u www-data >/dev/null 2>&1; then
  useradd --system --no-create-home --shell /usr/sbin/nologin www-data
fi

chown -R www-data:www-data "$BASE_DIR"

echo "\nNext steps:" 
echo "1) Copy backend/ to $BACKEND_DIR and web/dist to $WEB_DIR/dist"
echo "2) Create $BACKEND_DIR/.env from deploy/env.example (set DJANGO_SECRET_KEY)"
echo "3) Run deploy/do_deploy.sh"
