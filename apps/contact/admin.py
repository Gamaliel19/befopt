from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_editable = ("status",)
    ordering = ("-created_at",)
    actions = ["mark_as_processed", "mark_as_new"]

    # Un message reçu via le formulaire public ne doit pas pouvoir être
    # modifié dans son contenu par l'administrateur — seul le statut est
    # éditable (via list_editable ci-dessus).
    readonly_fields = ("name", "email", "phone", "subject", "message", "created_at")

    fieldsets = (
        ("Message reçu", {
            "fields": ("name", "email", "phone", "subject", "message", "created_at"),
        }),
        ("Suivi", {
            "fields": ("status",),
        }),
    )

    def has_add_permission(self, request):
        # Les messages ne peuvent venir que du formulaire public.
        return False

    @admin.action(description="Marquer les messages sélectionnés comme traités")
    def mark_as_processed(self, request, queryset):
        updated = queryset.update(status=ContactMessage.Status.PROCESSED)
        self.message_user(request, f"{updated} message(s) marqué(s) comme traité(s).")

    @admin.action(description="Marquer les messages sélectionnés comme nouveaux")
    def mark_as_new(self, request, queryset):
        updated = queryset.update(status=ContactMessage.Status.NEW)
        self.message_user(request, f"{updated} message(s) marqué(s) comme nouveau(x).")
