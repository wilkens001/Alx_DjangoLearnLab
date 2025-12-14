# Quick Start Deployment Guide

## Heroku Deployment (Fastest Method)

### 1. Prerequisites
```bash
# Install Heroku CLI
# Windows: Download from https://devcenter.heroku.com/articles/heroku-cli
# Mac: brew install heroku/brew/heroku
# Linux: curl https://cli-assets.heroku.com/install.sh | sh
```

### 2. Deploy in 5 Minutes

```bash
# Login to Heroku
heroku login

# Navigate to project
cd social_media_api

# Create Heroku app
heroku create your-unique-app-name

# Add PostgreSQL database
heroku addons:create heroku-postgresql:mini

# Generate secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set environment variables (replace YOUR-SECRET-KEY with generated key)
heroku config:set SECRET_KEY="YOUR-SECRET-KEY"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=".herokuapp.com"
heroku config:set SECURE_SSL_REDIRECT=True
heroku config:set SESSION_COOKIE_SECURE=True
heroku config:set CSRF_COOKIE_SECURE=True

# Deploy
git push heroku master

# Run migrations
heroku run python manage.py migrate

# Create admin user
heroku run python manage.py createsuperuser

# Open your app
heroku open
```

### 3. Your API is Live! 🎉

Access your API at: `https://your-unique-app-name.herokuapp.com/api/`

### 4. Test Your Deployment

```bash
# Check if API is running
curl https://your-app-name.herokuapp.com/api/

# Register a test user
curl -X POST https://your-app-name.herokuapp.com/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"TestPass123!","bio":"Test user"}'
```

### 5. View Logs

```bash
heroku logs --tail
```

### 6. Useful Heroku Commands

```bash
# Restart app
heroku restart

# Access Django shell
heroku run python manage.py shell

# View config
heroku config

# Scale workers
heroku ps:scale web=1
```

---

## Alternative: DigitalOcean App Platform

### 1. Setup (via Web UI)

1. Go to https://cloud.digitalocean.com/
2. Click "Create" → "Apps"
3. Connect your GitHub repository
4. Select the `social_media_api` directory

### 2. Configuration

**Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

**Run Command:**
```bash
gunicorn --worker-tmp-dir /dev/shm social_media_api.wsgi
```

### 3. Add Database

1. Click "Add Resource" → "Database"
2. Select PostgreSQL
3. Choose a plan (starts at $15/month)

### 4. Environment Variables

Add in the UI:
- `SECRET_KEY`: (Generate with Django)
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: `.ondigitalocean.app`
- `SECURE_SSL_REDIRECT`: `True`
- `SESSION_COOKIE_SECURE`: `True`
- `CSRF_COOKIE_SECURE`: `True`

### 5. Deploy

Click "Deploy" and wait 5-10 minutes.

---

## Environment Variables Quick Reference

### Required
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,.herokuapp.com
DATABASE_URL=postgres://user:pass@host:port/dbname
```

### Security (Production)
```env
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

### Optional (AWS S3)
```env
USE_S3=True
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=us-east-1
```

---

## Troubleshooting Common Issues

### Issue: Static files not loading
```bash
heroku run python manage.py collectstatic --noinput
```

### Issue: Database errors
```bash
heroku run python manage.py migrate
```

### Issue: App not starting
```bash
heroku logs --tail
# Check for missing environment variables or syntax errors
```

### Issue: 500 Internal Server Error
```bash
# Check logs
heroku logs --tail

# Common fixes:
# 1. Verify SECRET_KEY is set
# 2. Run migrations
# 3. Check ALLOWED_HOSTS includes your domain
```

---

## Production Checklist

- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` is secure and secret
- [ ] `ALLOWED_HOSTS` configured
- [ ] Database is PostgreSQL (not SQLite)
- [ ] SSL/HTTPS enabled
- [ ] Environment variables set
- [ ] Migrations run
- [ ] Static files collected
- [ ] Superuser created
- [ ] API endpoints tested

---

## Next Steps

1. **Custom Domain:** Configure your own domain name
2. **Monitoring:** Set up error tracking (Sentry)
3. **Backups:** Configure automatic database backups
4. **CDN:** Use CloudFlare for static files
5. **Scaling:** Add more workers as traffic grows

---

For detailed instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)
