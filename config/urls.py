"""
Configuration racine des URLs. Chaque app expose ses propres routes via
un fichier urls.py inclus ci-dessous — pas de vue métier définie ici.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from apps.core.sitemaps import (
    FormationSitemap,
    NewsSitemap,
    PageSitemap,
    ServiceSitemap,
    StaticViewSitemap,
)

sitemaps = {
    "static": StaticViewSitemap,
    "pages": PageSitemap,
    "services": ServiceSitemap,
    "formations": FormationSitemap,
    "news": NewsSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", TemplateView.as_view(template_name="core/robots.txt", content_type="text/plain"), name="robots"),
    path("expertises/", include("apps.services.urls")),
    path("formations/", include("apps.formations.urls")),
    path("actualites/", include("apps.news.urls")),
    path("contact/", include("apps.contact.urls")),
    # apps.pages doit rester en dernier : son urlconf contient un motif
    # générique "<slug:slug>/" (pour À propos, Entreprises & Institutions,
    # etc.) qui intercepterait sinon les préfixes ci-dessus.
    path("", include("apps.pages.urls")),
]

# En développement uniquement : sert les fichiers media (images uploadées)
# directement par Django. En production, c'est le serveur web/CDN qui s'en
# charge (voir Phase 11 — déploiement).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
