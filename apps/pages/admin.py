from django.contrib import admin

from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "updated_at")
    list_filter = ("status",)
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Contenu", {
            "fields": ("title", "slug", "content", "status"),
            "description": (
                "Le slug détermine l'adresse de la page (ex. : \"a-propos\" pour /a-propos/). "
                "Statut \"Brouillon\" = page invisible pour les visiteurs, \"Publié\" = page en ligne."
            ),
        }),
        ("Référencement (SEO)", {
            "fields": ("seo_title", "meta_description", "og_image"),
            "description": "Laissez vide pour utiliser les réglages SEO par défaut du site.",
            "classes": ("collapse",),
        }),
        ("Informations", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
