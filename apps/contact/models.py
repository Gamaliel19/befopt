from django.db import models


class ContactMessage(models.Model):
    """
    Messages reçus via le formulaire de contact public. Consultables et
    marquables comme traités depuis Django Admin (section 19 et 21 du
    cahier des charges).
    """

    class Status(models.TextChoices):
        NEW = "new", "Nouveau"
        PROCESSED = "processed", "Traité"

    name = models.CharField("Nom", max_length=150)
    email = models.EmailField("E-mail")
    phone = models.CharField("Téléphone", max_length=30, blank=True)
    subject = models.CharField("Sujet", max_length=200, blank=True)
    message = models.TextField("Message")
    status = models.CharField(
        "Statut", max_length=10, choices=Status.choices, default=Status.NEW
    )
    created_at = models.DateTimeField("Reçu le", auto_now_add=True)

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.subject or 'sans sujet'}"
