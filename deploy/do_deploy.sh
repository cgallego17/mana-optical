#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

DOMAIN_ROOT="opticamana.com"
BASE_DIR="/var/www/mana"
BACKEND_DIR="$BASE_DIR/backend"
WEB_DIST_DIR="$BASE_DIR/web/dist"
VENV_DIR="$BACKEND_DIR/.venv"
REPO_UPDATE_SCRIPT="$BASE_DIR/repo/update.sh"

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

# Fix ownership so gunicorn (www-data) can write to its working directory
chown -R www-data:www-data "$BACKEND_DIR"
chown -R www-data:www-data "$BASE_DIR/web"

# Nginx site — keep SSL config if already installed, else use HTTP-only
install -d /etc/nginx/sites-available /etc/nginx/sites-enabled
NGINX_SITE=/etc/nginx/sites-available/mana
if grep -q "listen 443" "$NGINX_SITE" 2>/dev/null; then
  echo "SSL nginx config already active, skipping overwrite."
else
  cp -f "$SCRIPT_DIR/nginx.http.conf" "$NGINX_SITE"
fi
ln -sf "$NGINX_SITE" /etc/nginx/sites-enabled/mana
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

# systemd service
# "enable --now" NO reinicia un servicio que ya está activo, así que un
# gunicorn corriendo desde antes seguiría sirviendo código viejo para
# siempre. Se reinicia explícitamente para garantizar que siempre quede
# corriendo el código recién desplegado.
cp -f "$SCRIPT_DIR/mana-backend.service" /etc/systemd/system/mana-backend.service
systemctl daemon-reload
systemctl enable mana-backend
systemctl restart mana-backend

# Acceso rápido: permite correr "sudo mana-update" desde cualquier directorio
# en vez de tener que cd al checkout del repo primero.
if [[ -f "$REPO_UPDATE_SCRIPT" ]]; then
  chmod +x "$REPO_UPDATE_SCRIPT"
  ln -sf "$REPO_UPDATE_SCRIPT" /usr/local/bin/mana-update
fi

echo "\nRunning smoke test..."
bash "$SCRIPT_DIR/do_smoke_test.sh"

echo "\n========================================"
echo "Deploy completado! Ahora configurar SSL:"
echo "========================================"
echo "\nEjecutar: sudo bash $SCRIPT_DIR/do_ssl.sh"
echo "\nEsto instalará certificados SSL con Certbot"
echo "Asegúrate de que los DNS A records apunten a este servidor."

echo "\nDeployed." 
echo "- http://$DOMAIN_ROOT/" 
echo "- http://$DOMAIN_ROOT/api/ (should be JSON/404 from Django, not HTML)"
