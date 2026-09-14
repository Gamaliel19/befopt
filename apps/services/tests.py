from django.test import TestCase

from .models import Service


class ServiceModelTests(TestCase):
    def test_slug_is_auto_generated(self):
        service = Service.objects.create(
            title="Orientation Stratégique & Coaching",
            short_description="Accompagnement sur-mesure.",
        )
        self.assertEqual(service.slug, "orientation-strategique-coaching")

    def test_ordering_respects_order_field(self):
        Service.objects.create(title="B", short_description="x", order=2)
        Service.objects.create(title="A", short_description="x", order=1)
        titles = list(Service.objects.values_list("title", flat=True))
        self.assertEqual(titles, ["A", "B"])


class ServiceListViewTests(TestCase):
    def test_only_published_services_are_listed(self):
        Service.objects.create(title="Publié", short_description="x", status=Service.Status.PUBLISHED)
        Service.objects.create(title="Brouillon", short_description="x", status=Service.Status.DRAFT)
        response = self.client.get("/expertises/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["services"]), 1)
        self.assertContains(response, "Publié")
        self.assertNotContains(response, "Brouillon")


class ServiceDetailViewTests(TestCase):
    def test_draft_service_returns_404(self):
        service = Service.objects.create(title="Test", short_description="x", status=Service.Status.DRAFT)
        response = self.client.get(f"/expertises/{service.slug}/")
        self.assertEqual(response.status_code, 404)
