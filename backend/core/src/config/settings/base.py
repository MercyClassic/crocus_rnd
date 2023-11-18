import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = os.getenv('DEBUG', False) == 'True'

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')

SECRET_KEY = os.getenv('SECRET_KEY')

DEV_HOSTS = ['http://%s' % host for host in os.getenv('DEV_HOSTS').split(', ')]
PROD_HOSTS = ['https://%s' % host for host in os.getenv('PROD_HOSTS').split(', ')]

ALLOWED_HOSTS = [
    host for host in f"{os.getenv('DEV_HOSTS')}, {os.getenv('PROD_HOSTS')}".split(', ')
]

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
    # 3rd apps
    'corsheaders',
    'rest_framework',
    'cachalot',
    # local apps
    'products.apps.MainConfig',
    'payments.apps.PaymentsConfig',
    'accounts.apps.AccountsConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'config.middleware.LogUnexpectedErrorMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404',
]

# if DEBUG is True:
#     INSTALLED_APPS += ['debug_toolbar', 'silk']
#     MIDDLEWARE += [
#         'debug_toolbar.middleware.DebugToolbarMiddleware',
#         # 'silk.middleware.SilkyMiddleware',
#     ]
#     INTERNAL_IPS = [
#         '127.0.0.1',
#         'localhost',
#         '0.0.0.0',
#     ]

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
STATIC_ROOT = os.path.join(BASE_DIR, '../../../frontend/src/static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'accounts.AuthUser'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    *DEV_HOSTS,
    *PROD_HOSTS,
]
CSRF_TRUSTED_ORIGINS = [
    *DEV_HOSTS,
    *PROD_HOSTS,
]

CACHALOT_TIMEOUT = 30

if not DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': f'redis://{REDIS_HOST}:6379/1',
            'OPTIONS': {
                'PASSWORD': os.getenv('REDIS_PASSWORD'),
            },
        },
    }
