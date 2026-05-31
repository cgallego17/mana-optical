#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

DOMAIN="opticamana.com"
DOMAIN_WWW="www.opticamana.com"
BASE_DIR="/var/www/mana"

if [[ $EUID -ne 0 ]]; then
  echo "Run as root (sudo)" >&2
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y certbot python3-certbot-nginx

# Requires DNS A records already pointing to this droplet.
certbot --nginx -d "$DOMAIN" -d "$DOMAIN_WWW"
certbot renew --dry-run

# Switch from nginx.http.conf to nginx.conf (with SSL)
echo "\nSwitching Nginx config to HTTPS..."
cp -f "$SCRIPT_DIR/nginx.conf" /etc/nginx/sites-available/mana
nginx -t
systemctl reload nginx

echo "\nSSL installed for $DOMAIN and $DOMAIN_WWW"
echo "Nginx configured for HTTPS"
