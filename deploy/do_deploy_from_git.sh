#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/cgallego17/mana-optical.git"
BRANCH="main"

BASE_DIR="/var/www/mana"
REPO_DIR="$BASE_DIR/repo"
BACKEND_TARGET="$BASE_DIR/backend"
WEB_TARGET="$BASE_DIR/web"

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
( cd "$REPO_DIR/web" && npm ci && NODE_OPTIONS="${NODE_OPTIONS:-} --max-old-space-size=2048" npm run build )

# Sync backend + deploy files
echo "Syncing backend..."
rm -rf "$BACKEND_TARGET"
cp -R "$REPO_DIR/backend" "$BACKEND_TARGET"

echo "Syncing web dist..."
mkdir -p "$WEB_TARGET"
rm -rf "$WEB_TARGET/dist"
cp -R "$REPO_DIR/web/dist" "$WEB_TARGET/dist"

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
