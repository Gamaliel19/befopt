"""
Tests de sécurité transverses (section 22 du cahier des charges) :
accès admin, protection CSRF. Placés à la racine (tests/) car ils ne
sont spécifiques à aucune app en particulier.
"""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings

User = get_user_model()


class AdminAccessTests(TestCase):
    def test_admin_redirects_anonymous_user_to_login(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_admin_accessible_to_authenticated_staff(self):
        User.objects.create_superuser("admin", "admin@befopt.td", "test-pass-1234")
        self.client.login(username="admin", password="test-pass-1234")
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)

    def test_regular_user_cannot_access_admin(self):
        User.objects.create_user("visiteur", "visiteur@example.com", "test-pass-1234")
        self.client.login(username="visiteur", password="test-pass-1234")
        response = self.client.get("/admin/", follow=True)
        self.assertEqual(response.status_code, 200)
        # Un utilisateur non-staff ne doit voir aucun modèle listé.
        self.assertNotContains(response, "Réglages du site")


@override_settings(CSRF_COOKIE_SECURE=False)
class CsrfProtectionTests(TestCase):
    def test_contact_form_rejects_request_without_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.post("/contact/", {
            "name": "Jean", "email": "jean@example.com", "phone": "",
            "subject": "Test", "message": "Message de test.", "website": "",
        })
        self.assertEqual(response.status_code, 403)
