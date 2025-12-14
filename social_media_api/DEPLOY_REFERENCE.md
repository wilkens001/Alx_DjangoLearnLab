# 🚀 Deployment Quick Reference Card

## Heroku - 5 Minute Deploy

```bash
# 1. Setup
heroku login
heroku create YOUR-APP-NAME

# 2. Add Database
heroku addons:create heroku-postgresql:mini

# 3. Configure (Replace YOUR-SECRET-KEY)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
heroku config:set SECRET_KEY="YOUR-SECRET-KEY"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=".herokuapp.com"
heroku config:set SECURE_SSL_REDIRECT=True
heroku config:set SESSION_COOKIE_SECURE=True
heroku config:set CSRF_COOKIE_SECURE=True

# 4. Deploy
git push heroku master

# 5. Initialize
heroku run python manage.py migrate
heroku run python manage.py createsuperuser

# 6. Open
heroku open
```

**Your API:** `https://YOUR-APP-NAME.herokuapp.com/api/`

---

## Useful Heroku Commands

```bash
heroku logs --tail              # View live logs
heroku restart                  # Restart app
heroku run python manage.py shell  # Django shell
heroku config                   # View all config vars
heroku pg:backups:capture      # Backup database
heroku ps                       # View running dynos
```

---

## DigitalOcean App Platform

### Build Command:
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

### Run Command:
```bash
gunicorn --worker-tmp-dir /dev/shm social_media_api.wsgi
```

### Environment Variables:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=.ondigitalocean.app
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## API Endpoints

### Authentication
```bash
# Register
POST /api/accounts/register/
{"username": "user", "email": "user@example.com", "password": "Pass123!", "bio": "Bio"}

# Login (get token)
POST /api/accounts/login/
{"username": "user", "password": "Pass123!"}

# Use token in requests
curl -H "Authorization: Token YOUR-TOKEN" https://your-app.herokuapp.com/api/posts/
```

### Main Endpoints
- `GET /api/posts/` - List posts
- `POST /api/posts/` - Create post
- `POST /api/posts/{id}/like/` - Like post
- `POST /api/accounts/follow/{id}/` - Follow user
- `GET /api/feed/` - Personalized feed
- `GET /api/notifications/` - User notifications

---

## Environment Variables Checklist

### Required ✅
- [ ] `SECRET_KEY` - Generate with Django
- [ ] `DEBUG` - Set to `False`
- [ ] `ALLOWED_HOSTS` - Your domain(s)
- [ ] `DATABASE_URL` - Auto-set by hosting provider

### Security (Production) ✅
- [ ] `SECURE_SSL_REDIRECT=True`
- [ ] `SESSION_COOKIE_SECURE=True`
- [ ] `CSRF_COOKIE_SECURE=True`

### Optional (AWS S3) 📦
- [ ] `USE_S3=True`
- [ ] `AWS_ACCESS_KEY_ID`
- [ ] `AWS_SECRET_ACCESS_KEY`
- [ ] `AWS_STORAGE_BUCKET_NAME`
- [ ] `AWS_S3_REGION_NAME`

---

## Testing Your Deployment

```bash
# Health check
curl https://your-app.herokuapp.com/api/

# Register test user
curl -X POST https://your-app.herokuapp.com/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"Test123!","bio":"Test"}'

# Login
curl -X POST https://your-app.herokuapp.com/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"Test123!"}'
```

---

## Troubleshooting

### Issue: Static files not loading
```bash
heroku run python manage.py collectstatic --noinput
```

### Issue: Database errors
```bash
heroku run python manage.py migrate
```

### Issue: 500 errors
```bash
heroku logs --tail  # Check for missing SECRET_KEY or other config
```

### Issue: App not starting
```bash
# Verify Procfile exists
cat Procfile
# Should show: web: gunicorn social_media_api.wsgi --log-file -
```

---

## Files Overview

| File | Purpose |
|------|---------|
| `Procfile` | Heroku process configuration |
| `runtime.txt` | Python version (3.13.0) |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variables template |
| `gunicorn_config.py` | Gunicorn configuration |
| `nginx.conf` | Nginx reverse proxy config |
| `DEPLOYMENT.md` | Full deployment guide |
| `QUICK_DEPLOY.md` | Quick start guide |

---

## Pre-Deployment Checklist

- [ ] All tests passing (`python manage.py test`)
- [ ] `DEBUG=False` in production
- [ ] `SECRET_KEY` generated and set
- [ ] `ALLOWED_HOSTS` configured
- [ ] PostgreSQL database added
- [ ] Environment variables set
- [ ] Static files collected
- [ ] Migrations ready to run
- [ ] `.env` file NOT committed to git

---

## Post-Deployment

1. **Run Migrations:**
   ```bash
   heroku run python manage.py migrate
   ```

2. **Create Admin User:**
   ```bash
   heroku run python manage.py createsuperuser
   ```

3. **Test API:**
   - Visit: `https://your-app.herokuapp.com/api/`
   - Admin: `https://your-app.herokuapp.com/admin/`

4. **Monitor Logs:**
   ```bash
   heroku logs --tail
   ```

5. **Set Up Backups:**
   ```bash
   heroku pg:backups:schedule --at '02:00 UTC'
   ```

---

## Support

- **Documentation:** See `DEPLOYMENT.md` for detailed guides
- **Quick Start:** See `QUICK_DEPLOY.md`
- **Repository:** https://github.com/wilkens001/Alx_DjangoLearnLab

---

**Last Updated:** December 14, 2025
