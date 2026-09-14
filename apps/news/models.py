from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import PublishableModel


class NewsArticle(PublishableModel):
    """
    Actualités BEFOPT. Comme pour Formation, la liste peut être vide au
    lancement — état vide géré côté template (Phase 7).
    """

    title = models.CharField("Titre", max_length=200)
    excerpt = models.CharField(
        "Chapô / résumé", max_length=255,
        help_text="Affiché dans la liste des actualités.",
    )
    content = models.TextField("Contenu")
    image = models.ImageField("Image", upload_to="news/", blank=True, null=True)
    image_alt_text = models.CharField(
        "Texte alternatif de l'image", max_length=200, blank=True,
        help_text="Décrit l'image pour l'accessibilité (obligatoire si une image est ajoutée).",
    )
    published_at = models.DateTimeField(
        "Date de publication", null=True, blank=True,
        help_text="Utilisée pour trier les actualités. Laisser vide pour utiliser la date de création.",
    )

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("news:detail", kwargs={"slug": self.slug})

    def clean(self):
        super().clean()
        if self.image and not self.image_alt_text:
            raise ValidationError(
                {"image_alt_text": "Obligatoire dès qu'une image est ajoutée (accessibilité)."}
            )
