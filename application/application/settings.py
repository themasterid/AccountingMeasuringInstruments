import os
from pathlib import Path

import environ

env = environ.Env()

environ.Env.read_env()

CSRF_TRUSTED_ORIGINS = ['http://62.84.115.143']

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env(
    'SECRET_KEY',
    default="unsafe-secret-key-45t548fh48fh4gefgh4734753erhg#$@#$")

DEBUG = env('DEBUG', default='True') == 'True'

LOGIN_URL = 'ppe:login'

LOGIN_REDIRECT_URL = 'ppe:index'

ALLOWED_HOSTS = env(
    'ALLOWED_HOSTS', default='localhost').split(', ')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users',
    'ppe',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'application.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'application.wsgi.application'

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': env(
                'DB_ENGINE',
                default='django.db.backends.postgresql'),
            'NAME': env(
                'POSTGRES_DB',
                default='postgres'),
            'USER': env(
                'POSTGRES_USER',
                default='postgres'),
            'PASSWORD': env(
                'POSTGRES_PASSWORD',
                default='postgres'),
            'HOST': env(
                'DB_HOST',
                default='db'),
            'PORT': env(
                'DB_PORT',
                default='5432'),
        }}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'),
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.User'

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = 'static/'

# STATICFILES_DIRS = [
#     BASE_DIR / 'static',
# ]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
