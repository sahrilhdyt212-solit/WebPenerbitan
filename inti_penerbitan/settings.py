"""
Django settings for inti_penerbitan project.
Optimized for Neon Postgres and Vercel Deployment.
"""

import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# --- SECURITY SETTINGS ---
SECRET_KEY = 'django-insecure-ht3(&*j1n96@bk%6^i&zuhkgahms95kozpquynb0=uv(w=w_c('

# Biarkan True saat di local, ganti False jika sudah benar-benar production
DEBUG = True

# Menambahkan domain Vercel dan wildcard biar akses lancar
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '172.20.10.2', '.vercel.app', '*']


# --- APPLICATION DEFINITION ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor', # Rich Text Editor
    'tulisan',  # App lo
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # WAJIB: Supaya CSS muncul di Vercel
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inti_penerbitan.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'inti_penerbitan.wsgi.application'


# --- DATABASE (NEON POSTGRES) ---
DATABASES = {
    'default': dj_database_url.config(
        default='postgres://neondb_owner:npg_hqbLd4ASUpG5@ep-billowing-base-aoaunaxx.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require',
        conn_max_age=600
    )
}


# --- PASSWORD VALIDATION ---
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


# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- STATIC & MEDIA FILES ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Settingan untuk mengumpulkan semua static file ke satu folder (Wajib buat Deployment)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise storage untuk optimasi pengiriman CSS/JS
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Setting Media untuk gambar/upload file
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# --- DEFAULT FIELD ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'