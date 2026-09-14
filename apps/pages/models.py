from django.db import models

from apps.core.models import PublishableModel


class Page(PublishableModel):
    """
    Pages de contenu semi-statique : "À propos", "Entreprises &
    Institutions", et toute page future de ce type — éditables depuis
    Django Admin sans intervention développeur.
    """

    title = models.CharField("Titre", max_length=200)
    content = models.TextField("Contenu")

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("pages:detail", kwargs={"slug": self.slug})
