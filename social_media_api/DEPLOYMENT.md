# Social Media API - Deployment Guide

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Deployment Options](#deployment-options)
4. [Heroku Deployment](#heroku-deployment)
5. [AWS Deployment](#aws-deployment)
6. [DigitalOcean Deployment](#digitalocean-deployment)
7. [Environment Variables](#environment-variables)
8. [Post-Deployment Configuration](#post-deployment-configuration)
9. [Monitoring and Maintenance](#monitoring-and-maintenance)
10. [Troubleshooting](#troubleshooting)

---

## Overview

This guide provides comprehensive instructions for deploying the Social Media API to production environments. The application is a Django REST Framework-based API with token authentication, user management, posts, comments, likes, follows, and notifications.

**Tech Stack:**
- Django 5.2+
- Django REST Framework
- PostgreSQL (production database)
- Gunicorn (WSGI server)
- WhiteNoise (static files)
- Optional: AWS S3 (media files)

---

## Prerequisites

Before deploying, ensure you have:

1. **Python 3.13+** installed
2. **Git** installed and repository configured
3. **Account** on your chosen hosting platform (Heroku, AWS, DigitalOcean, etc.)
4. **Database** service (PostgreSQL recommended)
5. **Environment variables** configured (see [Environment Variables](#environment-variables))

---

## Deployment Options

### Option 1: Heroku (Recommended for beginners)
- **Pros:** Easy setup, free tier available, automatic SSL
- **Cons:** Limited free tier, can be expensive at scale

### Option 2: AWS Elastic Beanstalk
- **Pros:** Scalable, lots of AWS integrations
- **Cons:** More complex setup, costs can add up

### Option 3: DigitalOcean App Platform
- **Pros:** Good balance of simplicity and control
- **Cons:** No free tier

### Option 4: VPS (DigitalOcean Droplet, Linode, etc.)
- **Pros:** Full control, cost-effective at scale
- **Cons:** Requires more setup and maintenance

---

## Heroku Deployment

### Step 1: Install Heroku CLI

Download and install the Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli

### Step 2: Login to Heroku

```bash
heroku login
```

### Step 3: Create Heroku App

```bash
cd social_media_api
heroku create your-app-name
```

### Step 4: Add PostgreSQL Database

```bash
heroku addons:create heroku-postgresql:mini
```

### Step 5: Set Environment Variables

```bash
# Generate a secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set environment variables
heroku config:set SECRET_KEY="your-generated-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=".herokuapp.com"
heroku config:set DJANGO_SETTINGS_MODULE=social_media_api.settings_production
heroku config:set SECURE_SSL_REDIRECT=True
heroku config:set SESSION_COOKIE_SECURE=True
heroku config:set CSRF_COOKIE_SECURE=True
```

### Step 6: Deploy to Heroku

```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku master
```

### Step 7: Run Migrations

```bash
heroku run python manage.py migrate
```

### Step 8: Create Superuser

```bash
heroku run python manage.py createsuperuser
```

### Step 9: Open Your App

```bash
heroku open
```

Your API should now be live at: `https://your-app-name.herokuapp.com`

---

## AWS Deployment

### Option A: AWS Elastic Beanstalk

#### Step 1: Install EB CLI

```bash
pip install awsebcli
```

#### Step 2: Initialize EB Application

```bash
cd social_media_api
eb init -p python-3.13 social-media-api --region us-east-1
```

#### Step 3: Create Environment

```bash
eb create social-media-api-env
```

#### Step 4: Configure Environment Variables

```bash
eb setenv SECRET_KEY="your-secret-key" \
  DEBUG=False \
  ALLOWED_HOSTS=".elasticbeanstalk.com" \
  DJANGO_SETTINGS_MODULE=social_media_api.settings_production
```

#### Step 5: Deploy

```bash
eb deploy
```

#### Step 6: Set Up RDS Database

1. Go to AWS Console > RDS
2. Create PostgreSQL database
3. Note the connection details
4. Set DATABASE_URL environment variable:

```bash
eb setenv DATABASE_URL="postgres://username:password@endpoint:5432/dbname"
```

#### Step 7: Run Migrations

```bash
eb ssh
cd /var/app/current
source /var/app/venv/staging-LQM1lest/bin/activate
python manage.py migrate
exit
```

### Option B: AWS EC2 (Manual Setup)

See the [VPS Deployment](#vps-deployment) section below.

---

## DigitalOcean Deployment

### Option A: App Platform (Managed)

#### Step 1: Create App

1. Log in to DigitalOcean
2. Go to Apps > Create App
3. Connect your GitHub repository
4. Select `social_media_api` directory

#### Step 2: Configure App

**Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

**Run Command:**
```bash
gunicorn --worker-tmp-dir /dev/shm social_media_api.wsgi
```

#### Step 3: Add Database

1. Click "Add Resource" > "Database"
2. Select PostgreSQL
3. Choose a plan

#### Step 4: Set Environment Variables

Add these in the App Platform UI:
- `SECRET_KEY`: Your secret key
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: `.ondigitalocean.app`
- `DATABASE_URL`: (Auto-populated by database resource)

#### Step 5: Deploy

Click "Deploy" and wait for the build to complete.

### Option B: Droplet (VPS)

See [VPS Deployment](#vps-deployment) section below.

---

## VPS Deployment

This guide applies to DigitalOcean Droplets, Linode, AWS EC2, or any Ubuntu/Debian VPS.

### Step 1: Create and Access VPS

```bash
ssh root@your-server-ip
```

### Step 2: Update System

```bash
apt update && apt upgrade -y
```

### Step 3: Install Dependencies

```bash
apt install -y python3.13 python3.13-venv python3-pip postgresql postgresql-contrib nginx git
```

### Step 4: Create Database

```bash
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE social_media_db;
CREATE USER social_media_user WITH PASSWORD 'your-secure-password';
ALTER ROLE social_media_user SET client_encoding TO 'utf8';
ALTER ROLE social_media_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE social_media_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE social_media_db TO social_media_user;
\q
```

### Step 5: Create Application User

```bash
adduser --system --group --home /opt/social_media_api social_media
```

### Step 6: Clone Repository

```bash
cd /opt/social_media_api
sudo -u social_media git clone https://github.com/wilkens001/Alx_DjangoLearnLab.git .
cd social_media_api
```

### Step 7: Set Up Virtual Environment

```bash
sudo -u social_media python3.13 -m venv venv
sudo -u social_media venv/bin/pip install -r requirements.txt
```

### Step 8: Configure Environment Variables

```bash
sudo -u social_media nano /opt/social_media_api/.env
```

Add:
```env
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgres://social_media_user:your-secure-password@localhost:5432/social_media_db
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Step 9: Run Migrations and Collect Static Files

```bash
sudo -u social_media venv/bin/python manage.py migrate
sudo -u social_media venv/bin/python manage.py collectstatic --noinput
sudo -u social_media venv/bin/python manage.py createsuperuser
```

### Step 10: Configure Gunicorn Service

```bash
nano /etc/systemd/system/gunicorn.service
```

Add:
```ini
[Unit]
Description=Gunicorn daemon for social_media_api
After=network.target

[Service]
User=social_media
Group=social_media
WorkingDirectory=/opt/social_media_api/social_media_api
Environment="PATH=/opt/social_media_api/venv/bin"
ExecStart=/opt/social_media_api/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/opt/social_media_api/gunicorn.sock \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log \
    social_media_api.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
mkdir -p /var/log/gunicorn
chown social_media:social_media /var/log/gunicorn
systemctl start gunicorn
systemctl enable gunicorn
```

### Step 11: Configure Nginx

```bash
cp /opt/social_media_api/social_media_api/nginx.conf /etc/nginx/sites-available/social_media_api
```

Edit the file to update domain names:
```bash
nano /etc/nginx/sites-available/social_media_api
```

Enable the site:
```bash
ln -s /etc/nginx/sites-available/social_media_api /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Step 12: Set Up SSL with Let's Encrypt

```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d your-domain.com -d www.your-domain.com
```

### Step 13: Configure Firewall

```bash
ufw allow 'Nginx Full'
ufw allow OpenSSH
ufw enable
```

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Generate using `get_random_secret_key()` |
| `DEBUG` | Debug mode | `False` (production) |
| `ALLOWED_HOSTS` | Allowed hosts | `.herokuapp.com,your-domain.com` |
| `DATABASE_URL` | Database connection | `postgres://user:pass@host:port/db` |

### Security Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECURE_SSL_REDIRECT` | Redirect HTTP to HTTPS | `True` |
| `SESSION_COOKIE_SECURE` | Secure session cookies | `True` |
| `CSRF_COOKIE_SECURE` | Secure CSRF cookies | `True` |
| `SECURE_HSTS_SECONDS` | HSTS header duration | `31536000` (1 year) |

### Optional Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `USE_S3` | Use AWS S3 for media | `True` |
| `AWS_ACCESS_KEY_ID` | AWS access key | Your AWS key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Your AWS secret |
| `AWS_STORAGE_BUCKET_NAME` | S3 bucket name | `my-bucket` |
| `AWS_S3_REGION_NAME` | S3 region | `us-east-1` |

### Generating a Secret Key

**Method 1: Python Command**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Method 2: Django Shell**
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```

---

## Post-Deployment Configuration

### 1. Create Superuser

```bash
# Heroku
heroku run python manage.py createsuperuser

# VPS
sudo -u social_media venv/bin/python manage.py createsuperuser
```

### 2. Test API Endpoints

```bash
# Health check
curl https://your-domain.com/api/

# Register user
curl -X POST https://your-domain.com/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"Test123!@#","bio":"Test user"}'

# Login
curl -X POST https://your-domain.com/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"Test123!@#"}'
```

### 3. Configure AWS S3 (Optional)

If using S3 for media files:

1. Create S3 bucket
2. Configure bucket policy for public read access
3. Set environment variables:
   - `USE_S3=True`
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_STORAGE_BUCKET_NAME`
   - `AWS_S3_REGION_NAME`

### 4. Set Up Monitoring

#### Heroku

```bash
heroku addons:create papertrail
heroku addons:create newrelic
```

#### VPS

Install monitoring tools:
```bash
# Install Prometheus and Grafana
apt install -y prometheus grafana

# Or use external services like:
# - Datadog
# - New Relic
# - Sentry (for error tracking)
```

---

## Monitoring and Maintenance

### Logging

#### View Logs

**Heroku:**
```bash
heroku logs --tail
```

**VPS:**
```bash
tail -f /var/log/gunicorn/error.log
tail -f /var/log/nginx/error.log
```

#### Configure Django Logging

Logs are configured in `settings_production.py`. View with:

```bash
# Application logs
tail -f logs/django.log

# Gunicorn logs
tail -f /var/log/gunicorn/access.log
tail -f /var/log/gunicorn/error.log
```

### Database Backups

#### Heroku

```bash
# Create backup
heroku pg:backups:capture

# Download backup
heroku pg:backups:download

# Schedule automatic backups
heroku pg:backups:schedule --at '02:00 UTC'
```

#### VPS

Create backup script:
```bash
nano /opt/scripts/backup_db.sh
```

Add:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U social_media_user social_media_db > /opt/backups/db_backup_$DATE.sql
find /opt/backups/ -type f -mtime +7 -delete
```

Schedule with cron:
```bash
crontab -e
# Add: 0 2 * * * /opt/scripts/backup_db.sh
```

### Performance Monitoring

Monitor these metrics:
- **Response time:** Should be < 200ms for most endpoints
- **Error rate:** Should be < 1%
- **Database connections:** Monitor for connection leaks
- **Memory usage:** Watch for memory leaks
- **CPU usage:** Should stay below 70%

### Scaling

#### Heroku

```bash
# Scale web dynos
heroku ps:scale web=2

# Upgrade database
heroku addons:upgrade heroku-postgresql:standard-0
```

#### VPS

1. **Vertical scaling:** Increase CPU/RAM
2. **Horizontal scaling:** Add more servers with load balancer
3. **Database scaling:** Set up read replicas

---

## Troubleshooting

### Common Issues

#### 1. Static Files Not Loading

**Symptoms:** CSS/JS not loading, 404 errors for static files

**Solution:**
```bash
python manage.py collectstatic --noinput --clear
```

Check `STATIC_ROOT` and `STATIC_URL` settings.

#### 2. Database Connection Errors

**Symptoms:** "OperationalError: could not connect to server"

**Solution:**
- Verify `DATABASE_URL` is correct
- Check database is running
- Verify firewall rules allow connection

#### 3. 500 Internal Server Error

**Symptoms:** Generic 500 error

**Solution:**
```bash
# Check logs
heroku logs --tail  # Heroku
tail -f /var/log/gunicorn/error.log  # VPS

# Common causes:
# - Missing environment variables
# - Database migration not run
# - Secret key not set
```

#### 4. CORS Errors (if using frontend)

**Solution:**
Install and configure django-cors-headers:
```bash
pip install django-cors-headers
```

Add to `INSTALLED_APPS` and `MIDDLEWARE` in settings.

#### 5. SSL Certificate Issues

**Solution:**
```bash
# Renew Let's Encrypt certificate
certbot renew

# Test renewal
certbot renew --dry-run
```

### Debug Mode

**Never enable DEBUG=True in production!**

To debug production issues:
1. Check logs
2. Use Sentry or similar error tracking
3. Test locally with production settings:
   ```bash
   DEBUG=False python manage.py runserver
   ```

---

## Deployment Checklist

- [ ] All tests passing
- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` set to secure random value
- [ ] `ALLOWED_HOSTS` configured
- [ ] Database configured (PostgreSQL recommended)
- [ ] Static files configured
- [ ] Media files storage configured
- [ ] Environment variables set
- [ ] Migrations run
- [ ] Superuser created
- [ ] SSL/HTTPS enabled
- [ ] Security headers configured
- [ ] Monitoring set up
- [ ] Backup strategy implemented
- [ ] Documentation updated
- [ ] API endpoints tested

---

## Useful Commands

### Heroku

```bash
# View logs
heroku logs --tail

# Run Django commands
heroku run python manage.py <command>

# Access Django shell
heroku run python manage.py shell

# Restart app
heroku restart

# View config
heroku config

# Set config
heroku config:set KEY=VALUE
```

### VPS

```bash
# Restart services
systemctl restart gunicorn
systemctl restart nginx

# View status
systemctl status gunicorn
systemctl status nginx

# View logs
journalctl -u gunicorn -f
tail -f /var/log/nginx/error.log

# Run Django commands
sudo -u social_media venv/bin/python manage.py <command>
```

---

## Security Best Practices

1. **Keep secrets secret:** Never commit `.env` files
2. **Update dependencies:** Regularly update packages
3. **Use HTTPS:** Always use SSL in production
4. **Limit permissions:** Use least privilege principle
5. **Monitor logs:** Watch for suspicious activity
6. **Rate limiting:** Implement API rate limiting
7. **Input validation:** Validate all user inputs
8. **Regular backups:** Automate database backups
9. **Security headers:** Configure properly (done in settings)
10. **Database encryption:** Use encrypted connections

---

## Support and Resources

- **Django Documentation:** https://docs.djangoproject.com/
- **DRF Documentation:** https://www.django-rest-framework.org/
- **Heroku Django:** https://devcenter.heroku.com/articles/django-app-configuration
- **DigitalOcean Tutorials:** https://www.digitalocean.com/community/tutorials
- **AWS Documentation:** https://docs.aws.amazon.com/

---

## Live URL

After deployment, your API will be available at:

- **Heroku:** `https://your-app-name.herokuapp.com`
- **DigitalOcean:** `https://your-app-name.ondigitalocean.app`
- **Custom Domain:** `https://your-domain.com`

**API Endpoints:**
- Base URL: `https://your-domain.com/api/`
- Registration: `POST /api/accounts/register/`
- Login: `POST /api/accounts/login/`
- Posts: `GET /api/posts/`
- User Profile: `GET /api/accounts/profile/`
- Feed: `GET /api/feed/`
- Notifications: `GET /api/notifications/`

---

## Maintenance Schedule

**Daily:**
- Monitor logs for errors
- Check application performance

**Weekly:**
- Review security logs
- Check database performance
- Update dependencies if needed

**Monthly:**
- Review and update documentation
- Analyze usage patterns
- Plan for scaling if needed
- Test backup restoration

**Quarterly:**
- Security audit
- Performance optimization
- Update Django and dependencies
- Review and update SSL certificates

---

## Contact and Support

For issues or questions:
- GitHub Issues: https://github.com/wilkens001/Alx_DjangoLearnLab/issues
- Email: [Your Email]

---

**Last Updated:** December 14, 2025
**Version:** 1.0.0
