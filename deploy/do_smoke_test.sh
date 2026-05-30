#!/usr/bin/env bash
set -euo pipefail

DOMAIN_ROOT="opticamana.com"

if [[ $EUID -ne 0 ]]; then
  echo "Run as root (sudo)" >&2
  exit 1
fi

echo "[1/6] systemd: mana-backend"
if ! systemctl is-active --quiet mana-backend; then
  systemctl status mana-backend --no-pager
  exit 1
fi

echo "[2/6] nginx config"
nginx -t

echo "[3/6] HTTP / (SPA)"
code=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1/)
if [[ "$code" != "200" ]]; then
  echo "Expected 200 from http://127.0.0.1/ got $code" >&2
  exit 1
fi

echo "[4/6] HTTP /api/ (should not be HTML)"
ct=$(curl -sI http://127.0.0.1/api/ | tr -d '\r' | awk -F': ' 'tolower($1)=="content-type"{print tolower($2)}' | head -n1)
if echo "$ct" | grep -q "text/html"; then
  echo "API is returning HTML via nginx (proxy misconfigured)" >&2
  exit 1
fi

echo "[5/6] HTTP /api/catalogo/marcas/"
ct2=$(curl -sI http://127.0.0.1/api/catalogo/marcas/ | tr -d '\r' | awk -F': ' 'tolower($1)=="content-type"{print tolower($2)}' | head -n1)
if echo "$ct2" | grep -q "text/html"; then
  echo "Expected JSON for /api/catalogo/marcas/ but got HTML" >&2
  exit 1
fi

echo "[6/6] HTTPS (optional)"
if getent hosts "$DOMAIN_ROOT" >/dev/null 2>&1; then
  code_ssl=$(curl -s -o /dev/null -w "%{http_code}" https://"$DOMAIN_ROOT"/ || true)
  if [[ "$code_ssl" == "200" || "$code_ssl" == "301" || "$code_ssl" == "302" ]]; then
    echo "HTTPS seems reachable: $code_ssl"
  else
    echo "HTTPS check returned $code_ssl (may be OK if SSL not installed yet)"
  fi
else
  echo "DNS not resolvable for $DOMAIN_ROOT (skipping)"
fi

echo "OK: smoke test passed"
