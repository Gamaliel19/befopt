"""
Réglages Django communs à tous les environnements (développement et production).
Les valeurs spécifiques à un environnement sont définies dans development.py
ou production.py, qui importent ce fichier avec `from .base import *`.
"""

from pathlib import Path

from decouple import Csv, config

# BASE_DIR pointe vers la racine du projet (là où se trouve manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# La clé secrète et le mode DEBUG sont TOUJOURS définis via variables
# d'environnement (voir .env.example) : jamais codés en dur ici.
SECRET_KEY = config("DJANGO_SECRET_KEY")

import os

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    "befopt.onrender.com",
    "localhost",
    "127.0.0.1",
]
"""
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="", cast=Csv())
"""

# Applications installées.
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
]

LOCAL_APPS = [
    "apps.core",
    "apps.pages",
    "apps.services",
    "apps.formations",
    "apps.news",
    "apps.contact",
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Dossier de templates global (base.html, composants partagés) en
        # plus des dossiers "templates/" internes à chaque app.
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Injecte les coordonnées BEFOPT (SiteSettings) dans tous
                # les templates, sans avoir à les repasser dans chaque vue.
                "apps.core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Base de données : les identifiants viennent des variables d'environnement,
# jamais codés en dur. PostgreSQL est le moteur cible (section 26 du cahier
# des charges) ; SQLite reste possible en local via development.py si besoin.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="befopt"),
        "USER": config("DB_USER", default="befopt"),
        "PASSWORD": config("DB_PASSWORD", default=""),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalisation : site en français, fuseau horaire du Tchad.
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Africa/Ndjamena"
USE_I18N = True
USE_TZ = True

# Fichiers statiques (CSS/JS/images du projet).
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Fichiers médias (uploads administrables : images de services, formations,
# actualités...).
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Config e-mail par défaut (formulaire de contact) : surchargée en
# production avec un vrai backend SMTP (voir production.py).
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="contact@befopt.td")
CONTACT_RECIPIENT_EMAIL = config("CONTACT_RECIPIENT_EMAIL", default="deubarodrigue2018@gmail.com")
