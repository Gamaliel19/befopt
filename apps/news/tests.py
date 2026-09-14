from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .models import NewsArticle


class NewsArticleModelTests(TestCase):
    def test_image_without_alt_text_is_rejected(self):
        article = NewsArticle(
            title="Test", excerpt="résumé", content="contenu",
            image=SimpleUploadedFile("x.jpg", b"fake-bytes"),
        )
        with self.assertRaises(ValidationError):
            article.full_clean()


class NewsListViewTests(TestCase):
    def test_empty_state_is_shown_when_no_article_published(self):
        response = self.client.get("/actualites/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aucune actualité publiée")

    def test_draft_article_is_not_listed(self):
        NewsArticle.objects.create(
            title="Brouillon", excerpt="x", content="x", status=NewsArticle.Status.DRAFT
        )
        response = self.client.get("/actualites/")
        self.assertContains(response, "Aucune actualité publiée")
