from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView

from apps.formations.models import Formation
from apps.news.models import NewsArticle
from apps.services.models import Service

from .models import Page


class HomeView(TemplateView):
    """
    Page d'accueil : hero, présentation, expertises, atouts, vision, CTA
    (structure validée en Phase 2). Les listes ci-dessous ne remontent
    que le contenu publié, et se limitent à un aperçu (pas la liste
    complète, qui vit sur les pages dédiées).
    """

    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = Service.objects.filter(status=Service.Status.PUBLISHED)[:4]
        context["latest_news"] = NewsArticle.objects.filter(
            status=NewsArticle.Status.PUBLISHED
        )[:3]
        context["latest_formations"] = Formation.objects.filter(
            status=Formation.Status.PUBLISHED
        )[:3]
        return context


class PageDetailView(DetailView):
    """
    Affiche une Page administrable par son slug (À propos, Entreprises &
    Institutions, ou toute autre page future de ce type).
    """

    model = Page
    template_name = "pages/detail.html"
    context_object_name = "page"

    def get_object(self):
        return get_object_or_404(Page, slug=self.kwargs["slug"], status=Page.Status.PUBLISHED)
