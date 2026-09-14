from django.core import mail
from django.test import TestCase

from .models import ContactMessage


class ContactFormTests(TestCase):
    valid_data = {
        "name": "Jean Test",
        "email": "jean@example.com",
        "phone": "",
        "subject": "Demande d'information",
        "message": "Bonjour, je souhaite en savoir plus.",
        "website": "",
    }

    def test_valid_submission_creates_message_and_sends_email(self):
        response = self.client.post("/contact/", self.valid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ContactMessage.objects.filter(email="jean@example.com").exists())
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Demande d'information", mail.outbox[0].subject)

    def test_success_message_is_displayed(self):
        response = self.client.post("/contact/", self.valid_data, follow=True)
        self.assertContains(response, "bien été envoyé")

    def test_honeypot_field_blocks_submission(self):
        """Protection anti-spam (section 19) : un champ honeypot rempli doit
        rejeter silencieusement l'envoi, sans créer de message ni d'e-mail."""
        data = {**self.valid_data, "website": "http://spam.example"}
        self.client.post("/contact/", data)
        self.assertFalse(ContactMessage.objects.filter(email="jean@example.com").exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_missing_required_field_is_rejected(self):
        data = {**self.valid_data, "message": ""}
        self.client.post("/contact/", data)
        self.assertFalse(ContactMessage.objects.filter(email="jean@example.com").exists())

    def test_invalid_email_is_rejected(self):
        data = {**self.valid_data, "email": "pas-un-email"}
        self.client.post("/contact/", data)
        self.assertFalse(ContactMessage.objects.exists())


class ContactMessageAdminTests(TestCase):
    def test_contact_message_content_is_readonly_in_admin(self):
        """Un administrateur ne doit pas pouvoir modifier le contenu soumis par un visiteur."""
        from django.contrib.admin.sites import site
        from .admin import ContactMessageAdmin

        admin_instance = ContactMessageAdmin(ContactMessage, site)
        self.assertIn("message", admin_instance.readonly_fields)
        self.assertIn("email", admin_instance.readonly_fields)
