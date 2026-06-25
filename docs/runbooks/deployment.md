# Deployment Guide

This guide deploys OrganicMart on an Ubuntu VPS using Python, Django, Gunicorn,
Nginx, PostgreSQL, and static files collected by Django.

## Production Checklist

- Buy or prepare a domain name.
- Point the domain DNS `A` record to the server IP.
- Create a strong `DJANGO_SECRET_KEY`.
- Set `DJANGO_ALLOWED_HOSTS` to your real domain.
- Use PostgreSQL through `DATABASE_URL`.
- Set `DJANGO_SETTINGS_MODULE=config.settings.production`.
- Configure HTTPS using Certbot.
- Configure email before sending real order notifications.
- Add real Razorpay keys before accepting real payments.
- Back up PostgreSQL before every release.

## 1. Install Server Packages

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip postgresql postgresql-contrib nginx git
```

## 2. Create PostgreSQL Database

```bash
sudo -u postgres psql
```

Inside PostgreSQL:

```sql
CREATE DATABASE organicmart;
CREATE USER organicmart WITH PASSWORD 'replace-with-strong-password';
ALTER ROLE organicmart SET client_encoding TO 'utf8';
ALTER ROLE organicmart SET default_transaction_isolation TO 'read committed';
ALTER ROLE organicmart SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE organicmart TO organicmart;
\q
```

## 3. Upload Code And Create Virtual Environment

```bash
cd /var/www
sudo git clone <your-repository-url> organicmart
sudo chown -R $USER:$USER /var/www/organicmart
cd /var/www/organicmart
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Create `.env`

```bash
cp .env.example .env
nano .env
```

Minimum production values:

```env
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_SECRET_KEY=replace-with-a-long-random-secret
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_HSTS_SECONDS=31536000
DATABASE_URL=postgresql://organicmart:replace-with-strong-password@127.0.0.1:5432/organicmart
EMAIL_URL=consolemail://
DEFAULT_FROM_EMAIL=OrganicMart <noreply@yourdomain.com>
API_DOCS_ENABLED=False
```

## 5. Run Django Release Commands

```bash
source .venv/bin/activate
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py seed_catalog
python manage.py createsuperuser
python manage.py check
```

## 6. Configure Gunicorn Systemd Service

Create the service:

```bash
sudo nano /etc/systemd/system/organicmart.service
```

Paste:

```ini
[Unit]
Description=OrganicMart Django application
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/organicmart
EnvironmentFile=/var/www/organicmart/.env
ExecStart=/var/www/organicmart/.venv/bin/gunicorn config.wsgi:application --config /var/www/organicmart/infra/gunicorn/gunicorn.conf.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Permissions and startup:

```bash
sudo chown -R www-data:www-data /var/www/organicmart
sudo systemctl daemon-reload
sudo systemctl enable organicmart
sudo systemctl start organicmart
sudo systemctl status organicmart
```

## 7. Configure Nginx

Create:

```bash
sudo nano /etc/nginx/sites-available/organicmart
```

Use this, replacing the domain:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 20M;

    location /static/ {
        alias /var/www/organicmart/staticfiles/;
        expires 30d;
        add_header Cache-Control "public";
    }

    location /media/ {
        alias /var/www/organicmart/media/;
        expires 7d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable it:

```bash
sudo ln -s /etc/nginx/sites-available/organicmart /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 8. Enable HTTPS

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
sudo systemctl reload nginx
```

## 9. Verify Live Site

```bash
curl https://yourdomain.com/health/live/
curl https://yourdomain.com/health/ready/
```

Open these in the browser:

- `https://yourdomain.com/`
- `https://yourdomain.com/products/`
- `https://yourdomain.com/blog/`
- `https://yourdomain.com/accounts/register/`
- `https://yourdomain.com/admin/`

## 10. Release Updates

```bash
cd /var/www/organicmart
sudo -u www-data git pull
sudo -u www-data .venv/bin/pip install -r requirements.txt
sudo -u www-data .venv/bin/python manage.py migrate --noinput
sudo -u www-data .venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart organicmart
sudo systemctl reload nginx
```

## Troubleshooting

Check app logs:

```bash
sudo journalctl -u organicmart -n 100 --no-pager
```

Check Nginx:

```bash
sudo nginx -t
sudo tail -n 100 /var/log/nginx/error.log
```

Check database:

```bash
sudo -u postgres psql -d organicmart
```
