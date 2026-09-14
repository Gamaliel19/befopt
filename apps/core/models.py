from django.db import models
from django.utils.text import slugify


class SiteSettings(models.Model):
    """
    Réglages globaux du site (singleton) : un seul enregistrement doit
    exister, chargé partout via .load() (voir context_processors.py).
    """

    # Identité générale
    site_name = models.CharField(max_length=100, default="BEFOPT")
    tagline = models.CharField(
        "Slogan / accroche", max_length=255, blank=True,
        help_text="Ex. : Connecter le talent d'aujourd'hui aux technologies de pointe de demain.",
    )
    mission_text = models.TextField("Texte de mission", blank=True)

    # Coordonnées (issues du dépliant)
    phone_1 = models.CharField("Téléphone principal", max_length=30, blank=True)
    phone_2 = models.CharField("Téléphone secondaire", max_length=30, blank=True)
    email = models.EmailField("E-mail de contact", blank=True)
    address = models.CharField("Localisation", max_length=255, blank=True)
    bp = models.CharField("Boîte postale", max_length=100, blank=True)

    # Réseaux sociaux — aucun n'est fourni actuellement par BEFOPT ; les
    # champs restent vides tant qu'ils ne sont pas communiqués, et
    # n'apparaissent pas dans le footer si vides (logique gérée au niveau
    # du template, Phase 7).
    facebook_url = models.URLField("Facebook", blank=True)
    linkedin_url = models.URLField("LinkedIn", blank=True)
    twitter_url = models.URLField("X / Twitter", blank=True)

    footer_text = models.CharField(
        "Texte du footer", max_length=255, blank=True,
        help_text="Ex. : mention légale courte ou copyright. Laisser vide si non fourni.",
    )

    # Valeurs SEO par défaut, utilisées quand une page/service/formation/
    # actualité ne définit pas ses propres champs SEO.
    default_seo_title = models.CharField("Titre SEO par défaut", max_length=70, blank=True)
    default_meta_description = models.CharField(
        "Meta description par défaut", max_length=160, blank=True
    )
    default_og_image = models.ImageField(
        "Image de partage par défaut (Open Graph)", upload_to="site/", blank=True, null=True
    )

    class Meta:
        verbose_name = "Réglages du site"
        verbose_name_plural = "Réglages du site"

    def __str__(self):
        return self.site_name

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class PublishableModel(models.Model):
    """
    Socle abstrait partagé par Page, Service, Formation et NewsArticle :
    slug, statut de publication, champs SEO et horodatage. Évite de
    dupliquer ces champs dans chaque modèle (principe DRY, décision
    Phase 3).
    """

    class Status(models.TextChoices):
        DRAFT = "draft", "Brouillon"
        PUBLISHED = "published", "Publié"

    slug = models.SlugField("Slug (URL)", max_length=255, unique=True, blank=True)
    status = models.CharField(
        "Statut", max_length=10, choices=Status.choices, default=Status.DRAFT
    )

    seo_title = models.CharField(
        "Titre SEO", max_length=70, blank=True,
        help_text="Laisser vide pour utiliser le titre par défaut du réglage général.",
    )
    meta_description = models.CharField("Meta description", max_length=160, blank=True)
    og_image = models.ImageField(
        "Image de partage (Open Graph)", upload_to="og/", blank=True, null=True
    )

    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug and hasattr(self, "title"):
            self.slug = slugify(self.title)[:255]
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        return self.status == self.Status.PUBLISHED
