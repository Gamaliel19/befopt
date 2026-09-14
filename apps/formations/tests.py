from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .models import Formation


class FormationModelTests(TestCase):
    def test_image_without_alt_text_is_rejected(self):
        """Accessibilité (section 17) : impossible d'enregistrer une image sans texte alternatif."""
        formation = Formation(
            title="Test", description="desc",
            image=SimpleUploadedFile("x.jpg", b"fake-bytes"),
        )
        with self.assertRaises(ValidationError):
            formation.full_clean()

    def test_image_with_alt_text_is_accepted(self):
        formation = Formation(
            title="Test", description="desc",
            image=SimpleUploadedFile("x.jpg", b"fake-bytes"),
            image_alt_text="Description de l'image",
        )
        formation.full_clean()  # ne doit lever aucune exception

    def test_no_image_does_not_require_alt_text(self):
        formation = Formation(title="Test", description="desc")
        formation.full_clean()  # ne doit lever aucune exception


class FormationListViewTests(TestCase):
    def test_empty_state_is_shown_when_no_formation_published(self):
        response = self.client.get("/formations/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aucune formation publiée")

    def test_published_formation_is_listed(self):
        Formation.objects.create(title="Ingénierie", description="x", status=Formation.Status.PUBLISHED)
        response = self.client.get("/formations/")
        self.assertContains(response, "Ingénierie")
        self.assertNotContains(response, "Aucune formation publiée")
