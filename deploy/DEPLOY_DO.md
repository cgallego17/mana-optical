---
description: Deploy en DigitalOcean (Nginx + Gunicorn)
---

# Objetivo
Servir el SPA Vue y el backend Django bajo el mismo dominio:

- `/` -> Vue (estático)
- `/api/` -> Django (Gunicorn)
- `/static/` y `/media/` -> archivos del servidor

# 1) Preparar servidor (Ubuntu)
1. Instala dependencias:
   - python3-venv, python3-pip
   - nginx
   - nodejs/npm (solo si compilas en el server)
2. Crea estructura:
   - `/var/www/mana/backend`
   - `/var/www/mana/web`

# 2) Backend (Django)
1. Copia el backend a `/var/www/mana/backend`.
2. Crea venv y dependencias:
   - `python3 -m venv .venv`
   - `.venv/bin/pip install -r requirements.txt`
3. Crea `/var/www/mana/backend/.env` basado en `deploy/env.example`.
4. Migraciones + collectstatic:
   - `.venv/bin/python manage.py migrate`
   - `.venv/bin/python manage.py collectstatic --noinput`

# 3) Gunicorn (systemd)
1. Copia `deploy/mana-backend.service` a:
   - `/etc/systemd/system/mana-backend.service`
2. Ajusta rutas si tu proyecto no está en `/var/www/mana`.
3. Activa el servicio:
   - `sudo systemctl daemon-reload`
   - `sudo systemctl enable --now mana-backend`

# 4) Frontend (Vue)
Opción A (recomendada): compilar local y subir `dist/`.
- `cd web && npm ci && npm run build`
- Copia `web/dist` a `/var/www/mana/web/dist`

# 5) Nginx
1. Copia `deploy/nginx.conf` a:
   - `/etc/nginx/sites-available/mana`
2. Enlaza:
   - `sudo ln -s /etc/nginx/sites-available/mana /etc/nginx/sites-enabled/mana`
3. Prueba y recarga:
   - `sudo nginx -t`
   - `sudo systemctl reload nginx`

# 6) HTTPS
## Requisitos previos
- A records de `opticamana.com` y `www.opticamana.com` apuntando al droplet.
- Nginx configurado y sirviendo el sitio por HTTP.

## Certbot
1. Instala:
   - `sudo apt update`
   - `sudo apt install -y certbot python3-certbot-nginx`
2. Emite certificado:
   - `sudo certbot --nginx -d opticamana.com -d www.opticamana.com`
3. Verifica auto-renovación:
   - `sudo certbot renew --dry-run`

## Nginx
- Usa `deploy/nginx.conf` (ya incluye redirect 80->443 y rutas del certificado).
- Prueba y recarga:
  - `sudo nginx -t`
  - `sudo systemctl reload nginx`

# Checklist
- `/api/health/` o `/api/` responde JSON (Django)
- `/` carga SPA
- `/static/` sirve archivos de `collectstatic`
- `/admin/login` funciona y el panel consume `/api/...`
