"""
Sitemap XML du site (section 18 du cahier des charges). Chaque contenu
publiable expose ses entrées publiées, avec sa date de dernière
modification.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.formations.models import Formation
from apps.news.models import NewsArticle
from apps.pages.models import Page
from apps.services.models import Service


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = "monthly"

    def items(self):
        return ["pages:home", "services:list", "formations:list", "news:list", "contact:contact"]

    def location(self, item):
        return reverse(item)


class PageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Page.objects.filter(status=Page.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_at


class ServiceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Service.objects.filter(status=Service.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_at


class FormationSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Formation.objects.filter(status=Formation.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_at


class NewsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return NewsArticle.objects.filter(status=NewsArticle.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_at
