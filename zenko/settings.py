from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-79ttb8byh3(n+(pbp!_se%cz(v-lf5c#p9_-x((yu#k$_a)bu&'
DEBUG = True

ALLOWED_HOSTS = [
    "*",
    "127.0.0.1",
    "localhost",
    "192.168.0.101",  # local Wi-Fi IP
    ".ngrok-free.app",  # any ngrok free subdomain
    # legacy entries retained
    "10.238.136.22",
    "condylar-cheeringly-temika.ngrok-free.dev",
]

# ✅ CSRF trusted origins (for ngrok + localhost + LAN IP)
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://192.168.0.101:8000",
    # wildcard ngrok domains (Django 4+ requires scheme)
    "https://*.ngrok-free.app",
    # legacy entries retained
    "http://10.238.136.22:8000",
    "https://condylar-cheeringly-temika.ngrok-free.dev",
]

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'django_ckeditor_5',

    # Custom apps
    'home',
    'Authentication',
    'cart',
    'widget_tweaks',

    # Phone authentication apps
    'phonenumber_field',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_hotp',
    'django_otp.plugins.otp_static',

    # Allauth apps
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'Authentication.backends.PhoneEmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

ROOT_URLCONF = 'zenko.urls'

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

WSGI_APPLICATION = 'zenko.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'zenko_db',
        'USER': 'postgres',
        'PASSWORD': 'Zenko@2025',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'staticfiles')
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'staticfiles/media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'Authentication.CustomUser'

# Twilio SMS Configuration (You need to set these with your actual credentials)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'your_account_sid_here')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'your_auth_token_here')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '+1234567890')

# For testing, you can disable actual SMS sending
SMS_TESTING_MODE = True  # Set to False in production

# Login redirects
LOGIN_URL = '/authenticate/signin/'             # sign-in page
LOGIN_REDIRECT_URL = '/'   # after login redirect
LOGOUT_REDIRECT_URL = '/'

# Allauth settings
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']



# Use https when generating absolute URLs (for ngrok/public)
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
