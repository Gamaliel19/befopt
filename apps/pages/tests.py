from django.test import TestCase

from .models import Page


class PageModelTests(TestCase):
    def test_slug_is_auto_generated_from_title(self):
        page = Page.objects.create(title="À propos", content="Contenu.")
        self.assertEqual(page.slug, "a-propos")

    def test_default_status_is_draft(self):
        page = Page.objects.create(title="Test", content="Contenu.")
        self.assertEqual(page.status, Page.Status.DRAFT)
        self.assertFalse(page.is_published)


class HomeViewTests(TestCase):
    def test_home_page_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/home.html")


class PageDetailViewTests(TestCase):
    def test_published_page_is_accessible(self):
        Page.objects.create(
            title="À propos", slug="a-propos", content="Contenu.",
            status=Page.Status.PUBLISHED,
        )
        response = self.client.get("/a-propos/")
        self.assertEqual(response.status_code, 200)

    def test_draft_page_returns_404(self):
        """Une page en brouillon ne doit jamais être visible publiquement."""
        Page.objects.create(
            title="Brouillon", slug="brouillon", content="Contenu.",
            status=Page.Status.DRAFT,
        )
        response = self.client.get("/brouillon/")
        self.assertEqual(response.status_code, 404)

    def test_unknown_slug_returns_404(self):
        response = self.client.get("/page-inexistante/")
        self.assertEqual(response.status_code, 404)
