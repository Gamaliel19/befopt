from django.contrib import admin

from .models import NewsArticle


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "published_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "published_at"
    fieldsets = (
        ("Contenu", {
            "fields": ("title", "slug", "excerpt", "content", "status", "published_at"),
            "description": (
                "Statut \"Brouillon\" = actualité invisible pour les visiteurs. "
                "Laissez \"Date de publication\" vide pour trier par date de création."
            ),
        }),
        ("Image", {
            "fields": ("image", "image_alt_text"),
            "description": "Le texte alternatif est obligatoire dès qu'une image est ajoutée (accessibilité).",
        }),
        ("Référencement (SEO)", {
            "fields": ("seo_title", "meta_description", "og_image"),
            "classes": ("collapse",),
        }),
        ("Informations", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
