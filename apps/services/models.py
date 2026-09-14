from django.db import models

from apps.core.models import PublishableModel


class Service(PublishableModel):
    """
    Les 4 domaines d'expertise BEFOPT (Orientation Stratégique & Coaching,
    Ingénierie de Formation, Renforcement de Capacités, Passerelles
    Internationales). L'ordre d'affichage est géré par le champ `order`,
    modifiable depuis l'admin (Phase 6).
    """

    title = models.CharField("Titre", max_length=200)
    short_description = models.CharField(
        "Description courte", max_length=255,
        help_text="Affichée sur la page d'accueil (carte de service).",
    )
    content = models.TextField("Description détaillée", blank=True)
    icon = models.CharField(
        "Icône", max_length=50, blank=True,
        help_text="Nom d'icône du set utilisé par le design system (défini en Phase 7).",
    )
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)

    class Meta:
        verbose_name = "Service / Expertise"
        verbose_name_plural = "Services / Expertises"
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("services:detail", kwargs={"slug": self.slug})
