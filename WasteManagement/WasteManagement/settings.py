# # Add these at the top of your settings.py
# import os
# from dotenv import load_dotenv
# from urllib.parse import urlparse

# load_dotenv()

# # Replace the DATABASES section of your settings.py with this
# tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': tmpPostgres.path.replace('/', ''),
#         'USER': tmpPostgres.username,
#         'PASSWORD': tmpPostgres.password,
#         'HOST': tmpPostgres.hostname,
#         'PORT': 5432,
#     }
# }
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent


# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-2s2hkz86bf7pc6_n+t-jqa7+mkqny3h)syt2n*7%-fm8$)p!m5'

# DEBUG = False

# ALLOWED_HOSTS = ['*']
# AUTH_USER_MODEL = 'waste.CustomUser'

# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',  # Default authentication backend
# ]


# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     # 'waste',
#     'admin_app',
#     'csp',
#     'waste.apps.WasteConfig',
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     # 'csp.middleware.CSPMiddleware',
    
# ]

# ROOT_URLCONF = 'WasteManagement.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'WasteManagement.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'waste_management',
#         'USER': 'waste_user',
#         'PASSWORD': 'securepassword',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }



# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

# USE_I18N = True

# USE_TZ = True

# STATIC_URL = '/static/'

# # Add this if you want to serve static files from a custom folder
# STATICFILES_DIRS = [
#     BASE_DIR / 'static',
# ]


# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'
# LOGIN_URL = '/login/'  # Change this to match your login URL pattern
# AUTH_USER_MODEL = 'waste.CustomUser'
# # LOGIN_REDIRECT_URL = '/mobile-home/'   # Redirect here after successful login
# LOGIN_REDIRECT_URL = '/upload-photo/' 
# LOGOUT_REDIRECT_URL = '/'  # Redirect to homepage after logout

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#         'OPTIONS': {
#             'min_length': 8,
#         },
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


import os
import dj_database_url
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()  # Load environment variables from a .env file

BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')
CSRF_TRUSTED_ORIGINS = ['https://ecotrack-g7p0.onrender.com']

# Database Setup
DATABASE_URL = os.getenv("DATABASE_URL")  # Get the DATABASE_URL from environment variables

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,  # Optimized pooling
            ssl_require=True    # Required for Neon.tech
        )
    }
else:
    raise ValueError("DATABASE_URL is not set in environment variables")

# Static & Media Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

if os.path.exists(os.path.join(BASE_DIR, 'static')):
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
else:
    STATICFILES_DIRS = []

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Authentication
AUTH_USER_MODEL = 'waste.CustomUser'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/upload-photo/'
LOGOUT_REDIRECT_URL = '/'

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin_app',
    'csp',
    'waste.apps.WasteConfig',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Templates & WSGI
ROOT_URLCONF = 'WasteManagement.urls'
WSGI_APPLICATION = 'WasteManagement.wsgi.application'

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

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default Primary Key Field Type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
