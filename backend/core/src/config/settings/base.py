import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = os.environ['DEBUG'] == 'True'

REDIS_HOST = os.environ['REDIS_HOST']

RABBITMQ_HOST = os.environ['RABBITMQ_HOST']

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = json.loads(os.environ['ALLOWED_HOSTS'])

ROLLBAR = {
    'access_token': os.getenv('ROLLBAR_ACCESS_TOKEN'),
    'environment': 'development' if DEBUG else 'production',
    'root': str(BASE_DIR),
}


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'rest_framework',
]

if not DEBUG:
    THIRD_PARTY_APPS.append('cachalot')

INSTALLED_APPS += THIRD_PARTY_APPS

LOCAL_APPS = [
    'payments.application.django.apps.PaymentsConfig',
    'products.apps.ProductsConfig',
    'accounts.apps.AccountsConfig',
]

INSTALLED_APPS += LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'config.middlewares.log.LogUnexpectedErrorMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / '../../../frontend/src/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = 'accounts.AuthUser'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MIGRATION_MODULES = {
    'payments': 'payments.infrastructure.db.migrations',
}

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = json.loads(os.environ['CORS_ALLOWED_ORIGINS'])
CSRF_TRUSTED_ORIGINS = json.loads(os.environ['CSRF_TRUSTED_ORIGINS'])

CACHALOT_TIMEOUT = 30

if not DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': f'redis://{REDIS_HOST}:6379',
            'OPTIONS': {
                'PASSWORD': os.environ['REDIS_PASSWORD'],
            },
        },
    }
