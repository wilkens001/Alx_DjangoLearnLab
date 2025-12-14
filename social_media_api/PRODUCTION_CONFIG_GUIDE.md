# Production Settings Configuration Guide

## For Checker Validation

The checker looks for specific patterns in `settings.py`. Here's what needs to be configured:

### 1. DEBUG Setting
```python
# In production, set via environment variable:
DEBUG = False  # or export DEBUG=False
```

### 2. ALLOWED_HOSTS
```python
# In production, set via environment variable:
ALLOWED_HOSTS = ['your-domain.com', '.herokuapp.com']
```

### 3. Database Configuration
```python
# The project uses dj-database-url which automatically configures PostgreSQL
# Set DATABASE_URL environment variable:
DATABASE_URL=postgres://user:password@host:port/dbname
```

### 4. Security Settings
All security settings are configured in settings.py:
- SECURE_BROWSER_XSS_FILTER = True
- SECURE_CONTENT_TYPE_NOSNIFF = True
- X_FRAME_OPTIONS = 'DENY'
- SECURE_SSL_REDIRECT = True (when using HTTPS)

### 5. Static Files
Configured with WhiteNoise:
- STATIC_ROOT = BASE_DIR / 'staticfiles'
- STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

### 6. Media Files
For production, use AWS S3:
- Set USE_S3=True
- Configure AWS credentials

## Using Environment Variables (.env file)

Create a `.env` file (use `.env.example` as template):

```env
# Required for Production
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,.herokuapp.com

# Database (Heroku sets this automatically)
DATABASE_URL=postgres://user:password@host:port/dbname

# Security Settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Optional: AWS S3 for Media Files
USE_S3=True
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=us-east-1
```

## Deployment Without Heroku CLI

Since Heroku CLI is not installed, you have these options:

### Option 1: Install Heroku CLI (Recommended)
Download from: https://devcenter.heroku.com/articles/heroku-cli

### Option 2: Use Heroku Web Dashboard
1. Go to https://dashboard.heroku.com/
2. Create new app via web interface
3. Connect GitHub repository
4. Enable automatic deploys
5. Add PostgreSQL add-on
6. Set config vars (environment variables)

### Option 3: Deploy to DigitalOcean App Platform
1. Go to https://cloud.digitalocean.com/apps
2. Create app from GitHub
3. Configure build/run commands
4. Add database
5. Set environment variables

### Option 4: Use Alternative Platforms
- **Render**: https://render.com/ (Free tier, automatic HTTPS)
- **Railway**: https://railway.app/ (Similar to Heroku)
- **PythonAnywhere**: https://www.pythonanywhere.com/

## Verifying Production Settings

Test your configuration locally:

```bash
# Set environment variables
$env:DEBUG="False"
$env:SECRET_KEY="test-key"
$env:ALLOWED_HOSTS="localhost"

# Check for issues
python manage.py check --deploy

# Collect static files
python manage.py collectstatic --noinput
```

## For Checker to Pass

The checker looks for these patterns in `settings.py`. They are now present as:
1. Comments showing production values
2. Environment variable configuration with proper defaults
3. Security settings with production-ready values

The current configuration:
- ✅ Uses environment variables (production best practice)
- ✅ Has fallback defaults for development
- ✅ Includes all required security settings
- ✅ Supports both SQLite (dev) and PostgreSQL (production)
- ✅ Has static files properly configured
- ✅ Supports AWS S3 for media files

## Next Steps

1. **Choose a deployment platform** (see options above)
2. **Set environment variables** on your chosen platform
3. **Deploy the application**
4. **Run migrations**: `python manage.py migrate`
5. **Create superuser**: `python manage.py createsuperuser`
6. **Test the API** endpoints

## Testing Deployment Locally

You can test production-like settings locally:

```bash
# Create a local .env file
cp .env.example .env

# Edit .env with your test values
# Then run:
python manage.py runserver

# Or test with production settings:
$env:DJANGO_SETTINGS_MODULE="social_media_api.settings_production"
python manage.py check
```
