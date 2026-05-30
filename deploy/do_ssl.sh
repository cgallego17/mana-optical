#!/usr/bin/env bash
set -euo pipefail

DOMAIN="opticamana.com"
DOMAIN_WWW="www.opticamana.com"

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

echo "\nSSL installed for $DOMAIN and $DOMAIN_WWW"
