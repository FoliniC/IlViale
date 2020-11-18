"""
Django settings for IlViale project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import logging
import environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = ''

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'p$6-^4q-9@j2z!y^d^^5l3-nc_pvlh8*8ld&_(0!971-b6jvu('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_CONTENT_TYPE_NOSNIFF = False
X_FRAME_OPTIONS = 'DENY'

ALLOWED_HOSTS = ['*']

# SERVER_TYPE = 'DEV'
SITE_ID = 1


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'BlogView.apps.BlogViewConfig',
    'sitetree',
    'tinymce',
    'sorl.thumbnail',
    'newsletter',
    'django_user_agents',
    'django_ses',
    'cookielaw',
] 

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',

    ]

# SITETREE_CLS = 'IlViale.mysitetree.MySiteTree'

# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
USER_AGENTS_CACHE = 'default'

ROOT_URLCONF = 'IlViale.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'IlViale', 'templates'),
                 os.path.join(BASE_DIR, 'sito_statico', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                #'IlViale.context_base_url.baseurl',
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS = [
    {"django.core.context_processors.request",      
     "django.contrib.auth.context_processors.auth",}
    ]

WSGI_APPLICATION = 'IlViale.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'it'

TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'IlViale/static'),
        os.path.join(BASE_DIR, 'sito_statico'),
    ]
# Random secret key
import random
key_chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
SECRET_KEY = ''.join([
    random.SystemRandom().choice(key_chars) for i in range(50)
])

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s %(filename)s:%(lineno)s %(message)s',
            #'style': '{',
            # %(module) %(process:d) %(thread:d) 
            #'datefmt': "%d/%b/%Y %H:%M:%S",
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
   # [formatter_generic]
#format = %(created)f %(levelname)-5.5s [%(name)s] %(message)s
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file1': {
            'level': 'INFO',
            #'class': 'logging.FileHandler',    
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'ilviale.log'),
            'formatter': 'verbose',
            'maxBytes': 50*1024,
            'backupCount': 5    
        },
        # 'file': {
        #     'level': 'INFO',
        #     'class': 'logging.FileHandler',    
        #     'filename': os.path.join(BASE_DIR, 'ilviale.log'),
        #     'formatter': 'verbose',
        # },  
    },
    'loggers': {
         'newsletter': {
            'handlers': ['console',
                         'file1', ],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['console',
                         'file1', ],
            'level': 'INFO',
            'propagate': True,

        },
    },
}

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django_ses.SESBackend'
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')     #'AKIA4NPCGD67DG5UVZ5U'
AWS_SECRET_ACCESS_KEY = env('EMAIL_HOST_PASSWORD')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@vialeformica.org'
DEFAULT_FROM_EMAIL = 'info@vialeformica.org'
#AWS_SES_REGION_NAME = 'us-east-1'
#AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
# on unix > create a shell script in /etc/profile.d
# sudo nano /etc/profile.d/set_environment.sh   
# insert following line at the end
# export EMAIL_HOST_PASSWORD='your_password'
# in ubuntu with apache set environment variable in
# sudo nano /etc/apache2/envvars
# on windows > setx EMAIL_HOST_PASSWORD "your_password" /M

DEFAULT_CONFIRM_EMAIL = True
#NEWSLETTER_RICHTEXT_WIDGET = "tinymce.widgets.TinyMCE"
