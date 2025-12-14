# Deploying Without Heroku CLI

Since you don't have Heroku CLI installed, here are alternative deployment methods.

## Option 1: Deploy via Heroku Web Dashboard (Easiest)

### Step 1: Create Heroku Account
1. Go to https://signup.heroku.com/
2. Sign up for a free account

### Step 2: Create New App
1. Log in to https://dashboard.heroku.com/
2. Click "New" → "Create new app"
3. Enter app name (e.g., `my-social-media-api`)
4. Choose region (United States or Europe)
5. Click "Create app"

### Step 3: Connect GitHub Repository
1. In your app dashboard, go to "Deploy" tab
2. Under "Deployment method", click "GitHub"
3. Click "Connect to GitHub"
4. Search for your repository: `Alx_DjangoLearnLab`
5. Click "Connect"
6. Select branch: `master`

### Step 4: Add PostgreSQL Database
1. Go to "Resources" tab
2. In "Add-ons" search box, type "postgres"
3. Select "Heroku Postgres"
4. Choose "Mini" plan (free)
5. Click "Submit Order Form"

### Step 5: Configure Environment Variables
1. Go to "Settings" tab
2. Click "Reveal Config Vars"
3. Add these variables:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.herokuapp.com` |
| `SECURE_SSL_REDIRECT` | `True` |
| `SESSION_COOKIE_SECURE` | `True` |
| `CSRF_COOKIE_SECURE` | `True` |

**Note:** `DATABASE_URL` is automatically set by Heroku Postgres addon.

### Step 6: Deploy
1. Go back to "Deploy" tab
2. Scroll to "Manual deploy"
3. Click "Deploy Branch"
4. Wait for build to complete

### Step 7: Run Migrations
1. Go to "More" (top right) → "Run console"
2. Type: `python manage.py migrate`
3. Click "Run"

### Step 8: Create Superuser
1. Click "More" → "Run console"
2. Type: `python manage.py createsuperuser`
3. Follow prompts to create admin account

### Step 9: Access Your API
Your API is now live at: `https://your-app-name.herokuapp.com/api/`

---

## Option 2: Deploy to Render (Free Alternative)

Render offers free hosting similar to Heroku.

### Step 1: Create Render Account
1. Go to https://render.com/
2. Sign up with GitHub

### Step 2: Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select `Alx_DjangoLearnLab` repository
4. Configure:
   - **Name:** `social-media-api`
   - **Root Directory:** `social_media_api`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command:** `gunicorn social_media_api.wsgi:application`

### Step 3: Add PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Choose free plan
3. Note the connection details

### Step 4: Set Environment Variables
In your web service settings, add:

```
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=postgres://... (from database connection)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Step 5: Deploy
1. Click "Create Web Service"
2. Wait for deployment to complete

### Step 6: Run Commands
Use the Shell tab to run:
```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## Option 3: Deploy to Railway

### Step 1: Create Railway Account
1. Go to https://railway.app/
2. Sign in with GitHub

### Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose `Alx_DjangoLearnLab`

### Step 3: Add PostgreSQL
1. Click "+ New"
2. Select "Database" → "PostgreSQL"

### Step 4: Configure
1. In your service settings, add environment variables:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=.railway.app
   ```
2. Railway automatically sets `DATABASE_URL`

### Step 5: Deploy
Railway automatically deploys on push to GitHub.

---

## Option 4: Deploy to PythonAnywhere

### Step 1: Create Account
1. Go to https://www.pythonanywhere.com/
2. Sign up for free account

### Step 2: Upload Code
1. Go to "Files" tab
2. Upload your project or clone from GitHub:
   ```bash
   git clone https://github.com/wilkens001/Alx_DjangoLearnLab.git
   cd Alx_DjangoLearnLab/social_media_api
   ```

### Step 3: Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 social_media_env
pip install -r requirements.txt
```

### Step 4: Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Set:
   - **Source code:** `/home/yourusername/Alx_DjangoLearnLab/social_media_api`
   - **Working directory:** Same as above
   - **Virtualenv:** `/home/yourusername/.virtualenvs/social_media_env`

### Step 5: Configure WSGI
Edit WSGI configuration file to point to your Django app.

### Step 6: Set Environment Variables
In web app settings, add environment variables.

---

## Option 5: Install Heroku CLI (Recommended for Full Control)

If you want to use the Heroku CLI commands:

### For Windows:
1. **Download installer:**
   - Go to https://devcenter.heroku.com/articles/heroku-cli
   - Click "Download and install"
   - Run the installer

2. **Or use Chocolatey:**
   ```powershell
   choco install heroku-cli
   ```

3. **Or use npm:**
   ```powershell
   npm install -g heroku
   ```

### Verify Installation:
```powershell
heroku --version
```

### Then follow original deployment commands:
```bash
heroku login
heroku create your-app-name
heroku addons:create heroku-postgresql:mini
heroku config:set SECRET_KEY="..." DEBUG=False
git push heroku master
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

---

## Comparison of Options

| Platform | Free Tier | Ease of Use | Database | SSL | CLI Required |
|----------|-----------|-------------|----------|-----|--------------|
| **Heroku (Web)** | Yes | ⭐⭐⭐⭐⭐ | Included | Auto | No |
| **Render** | Yes | ⭐⭐⭐⭐ | Separate | Auto | No |
| **Railway** | Limited | ⭐⭐⭐⭐ | Included | Auto | No |
| **PythonAnywhere** | Yes | ⭐⭐⭐ | MySQL only | Manual | No |
| **Heroku (CLI)** | Yes | ⭐⭐⭐⭐⭐ | Included | Auto | Yes |

---

## Recommended: Heroku Web Dashboard

For the easiest deployment without CLI:
1. Use Heroku Web Dashboard (Option 1)
2. It's free, has automatic SSL, includes PostgreSQL
3. No CLI installation needed
4. Everything done through web interface

---

## Testing Your Deployment

Once deployed, test your API:

```bash
# Check API root
curl https://your-app-name.herokuapp.com/api/

# Register a user
curl -X POST https://your-app-name.herokuapp.com/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"Test123!@#","bio":"Test"}'

# Login
curl -X POST https://your-app-name.herokuapp.com/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"Test123!@#"}'
```

---

## Troubleshooting

### Issue: Build fails
- Check that `requirements.txt` is in the root of `social_media_api` directory
- Verify all dependencies are listed

### Issue: Static files not loading
- Ensure `whitenoise` is installed
- Check `STATIC_ROOT` is set
- Run `python manage.py collectstatic`

### Issue: Database connection errors
- Verify `DATABASE_URL` is set (automatic on Heroku/Render)
- Check database addon is provisioned

### Issue: Application crashes
- Check logs (on Heroku: More → View logs)
- Verify all environment variables are set
- Ensure migrations have been run

---

## Next Steps

1. **Choose a platform** from the options above
2. **Follow the step-by-step guide** for that platform
3. **Set environment variables** as specified
4. **Deploy and test** your application
5. **Run migrations and create superuser**
6. **Access your live API!**

Your application is ready to deploy - all configuration is complete!
