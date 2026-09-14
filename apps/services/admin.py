from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "status", "updated_at")
    list_editable = ("order", "status")
    list_filter = ("status",)
    search_fields = ("title", "short_description", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    ordering = ("order", "title")
    fieldsets = (
        ("Contenu", {
            "fields": ("title", "slug", "short_description", "content", "status"),
            "description": (
                "La description courte apparaît sur la carte de la page d'accueil. "
                "Le contenu détaillé apparaît sur la fiche complète du service."
            ),
        }),
        ("Présentation", {
            "fields": ("icon", "order"),
            "description": "\"Ordre d'affichage\" contrôle la position de la carte (0 = premier).",
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
