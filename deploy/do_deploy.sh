#!/usr/bin/env bash
set -euo pipefail

DOMAIN_ROOT="opticamana.com"
BASE_DIR="/var/www/mana"
BACKEND_DIR="$BASE_DIR/backend"
WEB_DIST_DIR="$BASE_DIR/web/dist"
VENV_DIR="$BACKEND_DIR/.venv"

if [[ $EUID -ne 0 ]]; then
  echo "Run as root (sudo)" >&2
  exit 1
fi

if [[ ! -f "$BACKEND_DIR/manage.py" ]]; then
  echo "Backend not found at $BACKEND_DIR/manage.py" >&2
  exit 1
fi

if [[ ! -d "$WEB_DIST_DIR" ]]; then
  echo "Frontend dist not found at $WEB_DIST_DIR" >&2
  exit 1
fi

# Python deps
python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r "$BACKEND_DIR/requirements.txt"

# Django migrate + static
"$VENV_DIR/bin/python" "$BACKEND_DIR/manage.py" migrate
"$VENV_DIR/bin/python" "$BACKEND_DIR/manage.py" collectstatic --noinput

# Nginx site
install -d /etc/nginx/sites-available /etc/nginx/sites-enabled
cp -f "$BACKEND_DIR/../deploy/nginx.conf" /etc/nginx/sites-available/mana
ln -sf /etc/nginx/sites-available/mana /etc/nginx/sites-enabled/mana
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

# systemd service
cp -f "$BACKEND_DIR/../deploy/mana-backend.service" /etc/systemd/system/mana-backend.service
systemctl daemon-reload
systemctl enable --now mana-backend

echo "\nDeployed. Test:" 
echo "- https://$DOMAIN_ROOT/" 
echo "- https://$DOMAIN_ROOT/api/ (should be JSON/404 from Django, not HTML)"
