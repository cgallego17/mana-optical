#!/usr/bin/env bash
set -euo pipefail

DOMAIN_ROOT="opticamana.com"
NGINX_SITE=/etc/nginx/sites-available/mana

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

# Si SSL ya está instalado, Nginx redirige todo el tráfico HTTP a HTTPS
# (return 301 en nginx.conf), así que las pruebas de contenido deben hacerse
# contra HTTPS local en vez de esperar la respuesta directa en el puerto 80.
if grep -q "listen 443" "$NGINX_SITE" 2>/dev/null; then
  SSL_ACTIVE=1
  CURL_BASE=(curl -s --resolve "$DOMAIN_ROOT:443:127.0.0.1" "https://$DOMAIN_ROOT")
else
  SSL_ACTIVE=0
  CURL_BASE=(curl -s -H "Host: $DOMAIN_ROOT" "http://127.0.0.1")
fi

echo "[3/6] $([[ $SSL_ACTIVE -eq 1 ]] && echo HTTPS || echo HTTP) / (SPA)"
code=$("${CURL_BASE[@]}/" -o /dev/null -w "%{http_code}")
if [[ "$code" != "200" ]]; then
  echo "Expected 200 from / got $code" >&2
  exit 1
fi

echo "[4/6] /api/catalogo/marcas/ (must be JSON)"
ct=$("${CURL_BASE[@]}/api/catalogo/marcas/" -I | tr -d '\r' | awk -F': ' 'tolower($1)=="content-type"{print tolower($2)}' | head -n1)
if ! echo "$ct" | grep -q "application/json"; then
  echo "Expected JSON for /api/catalogo/marcas/ but got '$ct'" >&2
  exit 1
fi

echo "[5/6] /api/ (should not be SPA HTML)"
body=$("${CURL_BASE[@]}/api/" | head -n 50)
if echo "$body" | grep -qi "<div id=\"app\">"; then
  echo "API path is serving SPA HTML (proxy misconfigured)" >&2
  exit 1
fi

echo "[6/6] HTTPS (public DNS, best-effort)"
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
