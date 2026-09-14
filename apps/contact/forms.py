from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """
    Formulaire de contact public. Inclut un champ "piège à spam"
    (honeypot) : invisible pour un humain via CSS, mais souvent rempli
    automatiquement par les robots — s'il est rempli, on rejette
    silencieusement l'envoi (section 19 : protection anti-spam).
    """

    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-honeypot", "tabindex": "-1", "autocomplete": "off"}),
        label="",
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 6}),
        }
        labels = {
            "name": "Nom complet",
            "email": "E-mail",
            "phone": "Téléphone (optionnel)",
            "subject": "Sujet",
            "message": "Votre message",
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("website"):
            # Le honeypot a été rempli : très probablement un robot.
            raise forms.ValidationError("Une erreur est survenue. Merci de réessayer.")
        return cleaned_data
