"""
Réglages pour le développement local (votre machine Windows).
Usage : DJANGO_SETTINGS_MODULE=config.settings.development (valeur par
défaut définie dans manage.py pour ce projet).
"""

from .base import *  # noqa: F401,F403

# En local, l'e-mail du formulaire de contact est simplement affiché dans
# la console au lieu d'être réellement envoyé — pratique pour tester sans
# configurer de vrai serveur SMTP tout de suite.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Autorise l'accès en local sans dépendre uniquement de la variable
# d'environnement, tout en la respectant si elle est définie.
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
