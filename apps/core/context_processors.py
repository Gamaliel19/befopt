"""
Rend l'objet SiteSettings (coordonnées, réseaux sociaux, textes globaux)
disponible dans TOUS les templates sans avoir à le repasser depuis chaque
vue — utilisé notamment par le header et le footer.
"""

from .models import SiteSettings


def site_settings(request):
    return {"site_settings": SiteSettings.load()}
