"""
Django settings for personalized_trip_planner project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-your-very-secret-key-here")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',             
    'trip_planner_app',
    'router',           # <--- NEW APP ADDED
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

ROOT_URLCONF = 'personalized_trip_planner.urls'

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

WSGI_APPLICATION = 'personalized_trip_planner.wsgi.application'
ASGI_APPLICATION = 'personalized_trip_planner.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ... (rest of validation/i18n settings) ...

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Custom API Keys (loaded from .env)
TRAVEL_API_KEY = os.getenv("TRAVEL_API_KEY")
ACCOMMODATION_API_KEY = os.getenv("ACCOMMODATION_API_KEY")
ATTRACTIONS_API_KEY = os.getenv("ATTRACTIONS_API_KEY")
FOOD_API_KEY = os.getenv("FOOD_API_KEY")
GEN_AI_API_KEY = os.getenv("GEMINI_API_KEY") # Ensure using GEMINI_API_KEY alias if that's in .env
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY") # <--- NEW
OPENTRIPMAP_KEY = os.getenv("OPENTRIPMAP_KEY")       # <--- NEW

# AI Client Configuration
USE_MOCK_AI_CLIENT = os.getenv("USE_MOCK_AI_CLIENT", "False") == "True"


# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True