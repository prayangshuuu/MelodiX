from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = 'django-insecure-2+xb6ik@!a=soujx7dov7w5zh!%+f=n$hn+#qkchw*t1w6l-2#'
DEBUG = True  # Set DEBUG to True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Installed applications
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom apps
    'melodixapp.apps.MelodixappConfig',

    # Two-step authentication dependencies
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
    'two_factor',
    'qrcode',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files with WhiteNoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',  # Middleware for two-step authentication
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL configuration
ROOT_URLCONF = 'MelodiX.urls'

# Template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Global templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'MelodiX.context_processors.media_url',  # Custom context processor for MEDIA_URL
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'MelodiX.wsgi.application'

# Database configuration (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'melodixxx',
        'USER': 'prayangshu777',
        'PASSWORD': '777!!MLDXuvv',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Authentication settings
AUTH_USER_MODEL = 'melodixapp.User'  # Custom user model
LOGIN_URL = '/login/'  # URL for login
LOGIN_REDIRECT_URL = '/dashboard/'  # Redirect after login
LOGOUT_REDIRECT_URL = '/logout/'  # Redirect to custom logout page

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and media files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Directory for static files
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directory where static files are collected

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Directory for media files

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Two-factor authentication settings
TWO_FACTOR_CALL_GATEWAY = None  # Disable call-based OTP
TWO_FACTOR_SMS_GATEWAY = None  # Disable SMS-based OTP

# Session settings
SESSION_COOKIE_AGE = 1800  # Session timeout (30 minutes)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Expire session on browser close

# Static file compression with WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Debug Toolbar (Optional for development)
if DEBUG:
    INTERNAL_IPS = [
        '127.0.0.1',
    ]

# Custom 404 error handling
def show_custom_404(request, exception):
    """Custom 404 error page."""
    from django.shortcuts import render
    return render(request, 'errors/404.html', status=404)

# Set the custom 404 handler
handler404 = 'melodixapp.views.custom_404_view'
