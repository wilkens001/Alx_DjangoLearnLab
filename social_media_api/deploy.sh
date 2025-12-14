#!/bin/bash

# Deployment script for social_media_api
# This script helps automate the deployment process

echo "Starting deployment preparation..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser (optional - comment out if not needed)
# echo "Creating superuser..."
# python manage.py createsuperuser

echo "Deployment preparation complete!"
echo "Remember to set environment variables in your hosting service."
