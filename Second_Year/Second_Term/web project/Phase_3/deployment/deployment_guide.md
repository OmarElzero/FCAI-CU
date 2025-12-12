# JobSearch Backend Deployment Guide

This guide walks through the steps to deploy the JobSearch Django backend to a production server.

## Prerequisites

- Linux server (Ubuntu/Debian recommended)
- Python 3.10 or higher
- PostgreSQL database
- Nginx web server
- Domain name (optional but recommended)
- SSL certificate (optional but recommended)

## 1. Server Setup

### Update Server Packages
```bash
sudo apt update
sudo apt upgrade -y
```

### Install Required Packages
```bash
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx certbot python3-certbot-nginx git
```

## 2. Database Setup

### Create PostgreSQL Database and User
```bash
sudo -u postgres psql

CREATE DATABASE jobsearch_db;
CREATE USER jobsearch_user WITH PASSWORD 'your_strong_password';
ALTER ROLE jobsearch_user SET client_encoding TO 'utf8';
ALTER ROLE jobsearch_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE jobsearch_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE jobsearch_db TO jobsearch_user;
\q
```

## 3. Clone and Set Up the Project

### Create a Directory for the Project
```bash
mkdir -p /var/www/jobsearch
cd /var/www/jobsearch
```

### Clone the Repository (if using Git)
```bash
git clone your_repository_url .
```

### Alternatively, Upload Your Project Files
Upload your project files to the server using SFTP or SCP.

### Set Up Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Install PostgreSQL Adapter
```bash
pip install psycopg2-binary
```

## 4. Configure Environment Variables

### Create .env File
```bash
touch .env
```

### Add Environment Variables to .env
```
DJANGO_SETTINGS_MODULE=deployment.production_settings
DJANGO_SECRET_KEY=your_generated_secret_key
DB_NAME=jobsearch_db
DB_USER=jobsearch_user
DB_PASSWORD=your_strong_password
DB_HOST=localhost
DB_PORT=5432
```

## 5. Set Up Project for Production

### Create the Deployment Directory Structure
```bash
mkdir -p deployment/static deployment/media logs
```

### Copy and Adjust the Production Settings
Copy the production_settings.py file to the deployment directory and adjust as needed.

### Collect Static Files
```bash
python manage.py collectstatic --settings=deployment.production_settings
```

### Run Migrations
```bash
python manage.py migrate --settings=deployment.production_settings
```

### Create a Superuser (Admin)
```bash
python manage.py createsuperuser --settings=deployment.production_settings
```

## 6. Set Up Gunicorn

### Install Gunicorn
```bash
pip install gunicorn
```

### Create Gunicorn Socket File
```bash
sudo nano /etc/systemd/system/gunicorn.socket
```

Add:
```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

### Create Gunicorn Service File
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add:
```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/jobsearch
ExecStart=/var/www/jobsearch/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          --env DJANGO_SETTINGS_MODULE=deployment.production_settings \
          jobsearch.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Start and Enable Gunicorn
```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

## 7. Configure Nginx

### Create Nginx Configuration File
```bash
sudo nano /etc/nginx/sites-available/jobsearch
```

Add:
```
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/jobsearch/deployment;
    }

    location /media/ {
        root /var/www/jobsearch/deployment;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

### Enable the Nginx Configuration
```bash
sudo ln -s /etc/nginx/sites-available/jobsearch /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 8. Set Up SSL (HTTPS)

### Obtain SSL Certificate with Certbot
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Follow the prompts to complete the certificate setup.

## 9. Set Permissions

### Set the Correct Permissions
```bash
sudo chown -R www-data:www-data /var/www/jobsearch
sudo chmod -R 755 /var/www/jobsearch
```

## 10. Final Steps

### Check Gunicorn Status
```bash
sudo systemctl status gunicorn
```

### Restart All Services
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### Check for Any Errors
```bash
sudo journalctl -u gunicorn
sudo tail -f /var/log/nginx/error.log
```

## 11. Maintenance and Updates

### Pull Updates (if using Git)
```bash
cd /var/www/jobsearch
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --settings=deployment.production_settings
python manage.py collectstatic --settings=deployment.production_settings
sudo systemctl restart gunicorn
```

### Backup the Database
```bash
pg_dump -U jobsearch_user -W -F t jobsearch_db > jobsearch_backup_$(date +\%Y\%m\%d).tar
```

## 12. Monitoring and Analytics (Optional)

Consider setting up:
- Prometheus for metrics
- Grafana for visualization
- Sentry for error tracking

## 13. Security Considerations

- Keep all packages updated
- Set up a firewall (e.g., UFW)
- Configure fail2ban for protection against brute force attacks
- Regular security audits and updates

For any issues or questions, refer to the official Django documentation on deployment:
https://docs.djangoproject.com/en/5.2/howto/deployment/
