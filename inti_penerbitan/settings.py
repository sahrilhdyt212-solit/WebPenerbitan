"""
Django settings for inti_penerbitan project.
Optimized for Neon Postgres and Vercel Deployment.
"""

import os
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY SETTINGS ---
SECRET_KEY = 'django-insecure-ht3(&*j1n96@bk%6^i&zuhkgahms95kozpquynb0=uv(w=w_c('

# Biarkan True saat di local, ganti False jika sudah benar-benar production
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '172.20.10.2', '.vercel.app', '*']

# --- APPLICATION DEFINITION ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'ckeditor', # Rich Text Editor
    'tulisan',  # App lo
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # WAJIB buat Vercel
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
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- STATIC & MEDIA FILES ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise untuk optimasi CSS/JS di Vercel
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Konfigurasi Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dr9cnsucv',
    'API_KEY': '432311462277711',
    'API_SECRET': 'W_0iLFEoPsn_AFwBbPOvth5m9gU'
}

# Panggil config eksplisit agar CloudinaryField lancar
cloudinary.config( 
  cloud_name = CLOUDINARY_STORAGE['CLOUD_NAME'], 
  api_key = CLOUDINARY_STORAGE['API_KEY'], 
  api_secret = CLOUDINARY_STORAGE['API_SECRET'],
  secure = True
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'

# --- DEFAULT FIELD ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'