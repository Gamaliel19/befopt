from django.contrib import admin

from .models import SiteSettings

# Personnalisation générale de l'admin — pensé pour un utilisateur non
# développeur (section 11 du cahier des charges).
admin.site.site_header = "BEFOPT — Administration"
admin.site.site_title = "BEFOPT Admin"
admin.site.index_title = "Tableau de bord"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    SiteSettings est un singleton : un seul enregistrement existe, on
    masque "Ajouter" une fois qu'il est créé et on empêche sa suppression
    pour éviter qu'un utilisateur non technique casse le site par erreur.
    """

    fieldsets = (
        ("Identité", {
            "fields": ("site_name", "tagline", "mission_text"),
            "description": "Ces textes apparaissent sur la page d'accueil et dans le footer du site.",
        }),
        ("Coordonnées", {
            "fields": ("phone_1", "phone_2", "email", "address", "bp"),
        }),
        ("Réseaux sociaux", {
            "fields": ("facebook_url", "linkedin_url", "twitter_url"),
            "description": "Laissez vide un réseau que BEFOPT n'utilise pas — le lien n'apparaîtra pas sur le site.",
        }),
        ("Footer", {
            "fields": ("footer_text",),
        }),
        ("SEO par défaut", {
            "fields": ("default_seo_title", "default_meta_description", "default_og_image"),
            "description": "Utilisés uniquement quand une page ne définit pas ses propres réglages SEO.",
            "classes": ("collapse",),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Redirige directement vers l'unique enregistrement au lieu
        # d'afficher une liste à un seul élément — plus simple pour un
        # utilisateur non technique.
        obj = SiteSettings.load()
        from django.shortcuts import redirect
        return redirect("admin:core_sitesettings_change", obj.pk)
