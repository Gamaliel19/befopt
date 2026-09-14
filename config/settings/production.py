"""
Réglages pour la production. Toutes les valeurs sensibles viennent des
variables d'environnement du serveur — jamais de secret codé en dur ici.
"""

import dj_database_url
from decouple import config

from .base import *  # noqa: F401,F403

# Sécurité de base (section 20 du cahier des charges).
DEBUG = False

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# La plupart des PaaS (Render, Railway...) fournissent une variable
# DATABASE_URL toute prête plutôt que des identifiants séparés. On
# l'utilise si elle est présente, sinon on retombe sur les variables
# DB_* définies dans base.py (utile pour un VPS classique).
if config("DATABASE_URL", default=""):
    DATABASES["default"] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# Fichiers statiques servis directement par l'application via Whitenoise,
# sans dépendre d'un CDN externe dès le lancement (section 27).
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# Nécessaire derrière le proxy HTTPS d'un PaaS (Render/Railway terminent
# le TLS en amont et transmettent ce header).
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Envoi réel des e-mails du formulaire de contact via SMTP en production.
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
