"""
Django settings for LibraryProject project.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookshelf',
    'relationship_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',  # Content Security Policy middleware
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Media files (User uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Custom User Model
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================
# These settings implement Django security best practices to protect against
# common web vulnerabilities including XSS, CSRF, SQL injection, and clickjacking.

# DEBUG Setting
# SECURITY WARNING: Set to False in production to prevent exposure of sensitive
# information through error pages and stack traces.
# DEBUG = False  # Uncomment this line when deploying to production

# HTTPS and Cookie Security
# These settings ensure that security-sensitive cookies are only transmitted
# over HTTPS connections, preventing interception by attackers.
# NOTE: These should be enabled when using HTTPS in production
CSRF_COOKIE_SECURE = True  # Ensures CSRF cookie is only sent over HTTPS
SESSION_COOKIE_SECURE = True  # Ensures session cookie is only sent over HTTPS
SECURE_SSL_REDIRECT = False  # Set to True in production to redirect HTTP to HTTPS

# HTTP Strict Transport Security (HSTS)
# Forces browsers to only interact with the site over HTTPS for the specified duration
# This prevents protocol downgrade attacks and cookie hijacking
SECURE_HSTS_SECONDS = 31536000  # 1 year in seconds
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Apply HSTS to all subdomains
SECURE_HSTS_PRELOAD = True  # Allow inclusion in browser HSTS preload lists

# Browser Security Headers
# These headers provide additional layers of protection against various attacks

# X-Content-Type-Options: Prevents MIME-sniffing attacks
# Stops browsers from trying to guess content types, which could lead to XSS
SECURE_CONTENT_TYPE_NOSNIFF = True

# X-Frame-Options: Prevents clickjacking attacks
# Stops the site from being embedded in frames/iframes on other domains
X_FRAME_OPTIONS = 'DENY'  # Options: 'DENY', 'SAMEORIGIN'

# X-XSS-Protection: Enables browser's built-in XSS filter
# Provides an additional layer of XSS protection in older browsers
SECURE_BROWSER_XSS_FILTER = True

# CSRF Protection Settings
# Cross-Site Request Forgery protection is enabled by default via middleware
# Additional settings for enhanced CSRF protection:
CSRF_COOKIE_HTTPONLY = False  # Must be False for JavaScript to read it if needed
CSRF_USE_SESSIONS = False  # Set to True to store CSRF token in session instead of cookie
CSRF_COOKIE_SAMESITE = 'Strict'  # Prevents CSRF cookie from being sent with cross-site requests
SESSION_COOKIE_SAMESITE = 'Strict'  # Prevents session cookie from being sent with cross-site requests

# Session Security
# Additional session security settings to prevent session hijacking
SESSION_COOKIE_HTTPONLY = True  # Prevents JavaScript access to session cookie
SESSION_COOKIE_AGE = 3600  # Session expires after 1 hour of inactivity
SESSION_SAVE_EVERY_REQUEST = True  # Extends session on every request
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Session ends when browser closes

# Content Security Policy (CSP)
# CSP headers will be configured via middleware (see MIDDLEWARE setting above)
# This helps prevent XSS attacks by controlling which resources can be loaded

# Referrer Policy
# Controls how much referrer information is sent with requests
SECURE_REFERRER_POLICY = 'same-origin'  # Only send referrer for same-origin requests

# Additional Security Settings
# Allowed hosts must be properly configured in production
# ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']  # Configure for production

# ==============================================================================
# CONTENT SECURITY POLICY (CSP) CONFIGURATION
# ==============================================================================
# CSP helps prevent XSS attacks by specifying which sources of content are trusted.
# These directives control what resources the browser is allowed to load.

# Default source for all content types not explicitly defined
CSP_DEFAULT_SRC = ("'self'",)  # Only allow resources from same origin

# Script sources - controls where JavaScript can be loaded from
# 'unsafe-inline' should be avoided in production; use nonces or hashes instead
CSP_SCRIPT_SRC = ("'self'",)  # Only allow scripts from same origin

# Style sources - controls where CSS can be loaded from
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")  # Allow inline styles for now

# Image sources - controls where images can be loaded from
CSP_IMG_SRC = ("'self'", "data:", "https:")  # Allow images from same origin, data URIs, and HTTPS

# Font sources - controls where fonts can be loaded from
CSP_FONT_SRC = ("'self'", "https:", "data:")

# Connect sources - controls AJAX, WebSocket, and EventSource connections
CSP_CONNECT_SRC = ("'self'",)

# Media sources - controls <audio> and <video> sources
CSP_MEDIA_SRC = ("'self'",)

# Object sources - controls <object>, <embed>, and <applet> elements
CSP_OBJECT_SRC = ("'none'",)  # Disallow plugins

# Frame sources - controls where the site can be embedded in frames
CSP_FRAME_SRC = ("'self'",)

# Base URI - restricts URLs that can appear in <base> element
CSP_BASE_URI = ("'self'",)

# Form action - restricts URLs which can be used as form action targets
CSP_FORM_ACTION = ("'self'",)

# Frame ancestors - controls which sites can embed this site in frames
CSP_FRAME_ANCESTORS = ("'none'",)  # Prevent all framing (similar to X-Frame-Options: DENY)

# Upgrade insecure requests - automatically upgrade HTTP to HTTPS
CSP_UPGRADE_INSECURE_REQUESTS = True

# Include nonce in script and style tags for inline content
CSP_INCLUDE_NONCE_IN = ['script-src', 'style-src']
