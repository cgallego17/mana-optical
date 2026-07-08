#!/usr/bin/env bash
# Punto de entrada para actualizar el servidor de PRODUCCIÓN (droplet con
# Nginx + Gunicorn). Se ejecuta en el servidor, como root, parado dentro del
# checkout del repo (por convención /var/www/mana/repo):
#
#   cd /var/www/mana/repo && sudo bash update.sh
#
# Hace todo el trabajo delegando en el pipeline ya existente en deploy/, para
# no duplicar esa lógica:
#   deploy/do_deploy_from_git.sh
#     1) git pull del branch main
#     2) build del frontend (npm ci && npm run build)
#     3) sincroniza backend/ y web/dist a /var/www/mana
#     4) deploy/do_deploy.sh:
#          - pip install -r requirements.txt (en el venv del servidor)
#          - manage.py migrate
#          - manage.py collectstatic --noinput
#          - instala/recarga config de Nginx
#          - systemctl daemon-reload + enable --now mana-backend (gunicorn)
#          - smoke test (deploy/do_smoke_test.sh)
#
# Para desarrollo local en Windows (manage.py runserver) usa en su lugar:
#   cd backend && python manage.py migrate
#   cd web && npm run build   # para que Django sirva el build actualizado en :8000
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "${OS:-}" == "Windows_NT" ]]; then
  echo "update.sh es para el servidor de producción Linux (Nginx + Gunicorn)." >&2
  echo "En Windows solo tienes el entorno de desarrollo local; no hay gunicorn/nginx que reiniciar." >&2
  echo "Para actualizar tu entorno local usa: backend -> manage.py migrate, web -> npm run build." >&2
  exit 1
fi

if [[ $EUID -ne 0 ]]; then
  echo "Ejecuta como root: sudo bash update.sh" >&2
  exit 1
fi

exec bash "$ROOT_DIR/deploy/do_deploy_from_git.sh"
