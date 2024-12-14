
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2s2hkz86bf7pc6_n+t-jqa7+mkqny3h)syt2n*7%-fm8$)p!m5'

DEBUG = True

ALLOWED_HOSTS = []
AUTH_USER_MODEL = 'waste.CustomUser'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default authentication backend
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'waste',
    'admin_app',
    'csp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'csp.middleware.CSPMiddleware',
    
]

ROOT_URLCONF = 'WasteManagement.urls'

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

WSGI_APPLICATION = 'WasteManagement.wsgi.application'



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'waste_management',
        'USER': 'waste_user',
        'PASSWORD': 'securepassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

# Add this if you want to serve static files from a custom folder
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
LOGIN_URL = '/login/'  # Change this to match your login URL pattern
AUTH_USER_MODEL = 'waste.CustomUser'
# LOGIN_REDIRECT_URL = '/mobile-home/'   # Redirect here after successful login
LOGIN_REDIRECT_URL = '/upload-photo/' 
LOGOUT_REDIRECT_URL = '/'  # Redirect to homepage after logout

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# CSP_DEFAULT_SRC = ("'self'",)  # Default policy to restrict to self
# CSP_SCRIPT_SRC = ("'self'", "'nonce-{nonce}'")

# CSP_DEFAULT_SRC = ("'self'",)
# CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'",)  # Allow inline scripts
# CSP_STYLE_SRC = ("'self'", "'unsafe-inline'",)  # Allow inline styles
# CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://getbootstrap.com/")  # Allow inline styles

# CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "https://unpkg.com")  # Example of allowing external JS resources

# settings.py

# Define the Content Security Policy
# CSP_DEFAULT_SRC = ("'self'",)
# CSP_STYLE_SRC = ("'self'", "https://stackpath.bootstrapcdn.com", "https://cdnjs.cloudflare.com", "https://fonts.googleapis.com")
# CSP_SCRIPT_SRC = ("'self'", "https://code.jquery.com", "https://stackpath.bootstrapcdn.com", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com")
# CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
# CSP_IMG_SRC = ("'self'", "data:", "https://*")  # Allow images from any source, including inline images (data: URIs)

# CSP_INCLUDE_NONCES_IN = ["script-src", "style-src"]  # Use nonces for inline script and style execution
