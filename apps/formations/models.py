from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import PublishableModel


class Formation(PublishableModel):
    """
    Fiches de formation. La liste peut être vide au lancement — l'état
    vide est géré côté template (Phase 7), pas ici.
    """

    title = models.CharField("Titre", max_length=200)
    description = models.CharField(
        "Description courte", max_length=255,
        help_text="Affichée dans la liste des formations.",
    )
    content = models.TextField("Contenu détaillé", blank=True)
    image = models.ImageField("Image", upload_to="formations/", blank=True, null=True)
    image_alt_text = models.CharField(
        "Texte alternatif de l'image", max_length=200, blank=True,
        help_text="Décrit l'image pour l'accessibilité (obligatoire si une image est ajoutée).",
    )
    published_at = models.DateTimeField(
        "Date de publication", null=True, blank=True,
        help_text="Utilisée pour trier les formations. Laisser vide pour utiliser la date de création.",
    )

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("formations:detail", kwargs={"slug": self.slug})

    def clean(self):
        super().clean()
        if self.image and not self.image_alt_text:
            raise ValidationError(
                {"image_alt_text": "Obligatoire dès qu'une image est ajoutée (accessibilité)."}
            )
