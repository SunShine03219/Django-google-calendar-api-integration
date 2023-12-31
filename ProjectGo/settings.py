"""
Django settings for ProjectGo project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
import django_heroku
import dj_database_url


import ssl



# Import the required settings
from django.conf import settings
"""//
# CSRF HTTPS
# Enforce secure session cookies (only transmitted over HTTPS)
SESSION_COOKIE_SECURE = True
# Enforce secure CSRF cookies (only transmitted over HTTPS)
CSRF_COOKIE_SECURE = True
#
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
"""


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*6pahb^lg%8-oh^(@fp*r&is36$30&-#m0og@*u)1+6*qx5&1n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    
    'channels',
    'taggit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_heroku',
    'Communication',
    'Project',
    'Company',
    'Calendar',
    'bootstrap5',
    'django_user_agents',
    'stripe'
]

MIDDLEWARE = [
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ProjectGo.middleware.AppAllowedMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

ROOT_URLCONF = 'ProjectGo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['ProjectGo/design/templates', 
                 'ProjectGo/templates', 
                 'Project/Templates', 
                 'Communication/templates', 
                 'Company/templates',
                 ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'ProjectGo.wsgi.application'
ASGI_APPLICATION = 'ProjectGo.asgi.application'


host = [{
        'address': f'rediss://eu1-glorious-grackle-39638.upstash.io:39638',
        'password': '92c190f20bca455d9c8b3748763a3a5e',
    }]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
            #"hosts": host,
            "symmetric_encryption_keys": [SECRET_KEY],
            
        },
    },
    "ROUTING": "ProjectGo.routing.channel_routing",
    
    
}
MJML_BACKEND_MODE = "cmd"
MJML_EXEC_CMD = "node_modules/.bin/mjml"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'ProjectGo',
#         'USER': 'csadmin',
#         'PASSWORD': 'Pa$$w0rd',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '123qwe',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default authentication backend
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# https://docs.djangoproject.com/en/4.2/howto/static-files/



STATIC_URL          = '/static/'
STATICFILES_DIRS    = [BASE_DIR / 'ProjectGo/design/static/']
STATIC_ROOT         = BASE_DIR / 'staticfiles'

#STATIC_URL          = 'ProjectGo/design/static/'
#STATICFILES_DIRS    = ['ProjectGo/design/static/']


MEDIA_ROOT          = BASE_DIR / 'ProjectGo/Media'
MEDIA_URL           = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/projects/'

FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50MB

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

django_heroku.settings(locals())

CSRF_TRUSTED_ORIGINS = [
    'https://projectgo.herokuapp.com'
]


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'info@projectgo.lu'

