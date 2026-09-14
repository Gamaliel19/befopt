from django.test import TestCase

from .models import SiteSettings


class SiteSettingsTests(TestCase):
    def test_load_creates_singleton(self):
        """Le premier appel à load() crée l'enregistrement unique."""
        self.assertEqual(SiteSettings.objects.count(), 0)
        settings_obj = SiteSettings.load()
        self.assertEqual(SiteSettings.objects.count(), 1)
        self.assertEqual(settings_obj.pk, 1)

    def test_load_is_idempotent(self):
        """Appeler load() plusieurs fois ne crée jamais un deuxième enregistrement."""
        first = SiteSettings.load()
        second = SiteSettings.load()
        self.assertEqual(first.pk, second.pk)
        self.assertEqual(SiteSettings.objects.count(), 1)

    def test_context_processor_injects_site_settings(self):
        """SiteSettings doit être disponible dans le contexte de chaque page."""
        response = self.client.get("/")
        self.assertIn("site_settings", response.context)
