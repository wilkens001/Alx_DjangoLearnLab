# Deployment script for Windows PowerShell

Write-Host "Starting deployment preparation..." -ForegroundColor Green

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Collect static files
Write-Host "Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

# Run migrations
Write-Host "Running database migrations..." -ForegroundColor Yellow
python manage.py migrate

# Create superuser (optional - comment out if not needed)
# Write-Host "Creating superuser..." -ForegroundColor Yellow
# python manage.py createsuperuser

Write-Host "Deployment preparation complete!" -ForegroundColor Green
Write-Host "Remember to set environment variables in your hosting service." -ForegroundColor Cyan
