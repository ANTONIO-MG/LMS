"""
Django settings for MY_LEARNING_HUB project.
Generated by 'django-admin startproject' using Django 5.0.1.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*3j*(2(hpdvrr^7aqw!(8k7a05sv^i%s0ty6dys!cr+a^zm(rg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # added the dbbackup to backup my databases
    'dbbackup',
    # base is the main project that i am holding all the tasks
    'base',
    # this is the app that restores the save data from the backups
    'django_crontab',

    # the allauth authentication
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # clean up the duplicate files with teh following library
    'django_cleanup.apps.CleanupConfig',
    # python library for cellphone number fields
    "phonenumber_field",
    "crispy_forms",
    "crispy_bootstrap4",
    
]


DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': BASE_DIR / 'backup'}

CRONJOBS = [
    # change the number to change teh backup frequency in minutes
    ('*/10 * * * *', 'base.cron.my_backup')
    # please run teh following commands to get it working
    # python manage.py crondb start : start crontab
    # python manage.py db restore : restore to teh latest version of the database
    # python manage.py crontab add : add the current backup task
    # service cron restart  (on ubuntu)
    # python manage.py crondb show: show all teh currently active tasks
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'MY_LEARNING_HUB.urls'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1  # Add this if not already present, setting the ID of the current site

# Django Allauth settings
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_CHANGE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'http://localhost:8000/register/'



LOGIN_REDIRECT_URL = 'home'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION= True 
ACCOUNT_LOGOUT_ON_GET=True 
ACCOUNT_SIGNUP_REDIRECT_URL = 'register/'





TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'MY_LEARNING_HUB.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'base01',
        'HOST':  '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '27031992',
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

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# AUTH_USER_MODEL = 'base.Person'

# configure the different social accounts that you can authenticate by
SOCIALACCOUNT_PROVIDERS = {}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#CRISPY FORMS
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"