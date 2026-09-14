from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.core.models import SiteSettings

from .forms import ContactForm


class ContactView(FormView):
    template_name = "contact/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact:contact")

    def form_valid(self, form):
        # Le champ honeypot ne fait pas partie du modèle : on l'exclut
        # avant de sauvegarder le message reçu.
        contact_message = form.save()

        recipient = SiteSettings.load().email or settings.CONTACT_RECIPIENT_EMAIL
        send_mail(
            subject=f"[BEFOPT] Nouveau message de contact : {contact_message.subject or 'sans sujet'}",
            message=(
                f"Nom : {contact_message.name}\n"
                f"E-mail : {contact_message.email}\n"
                f"Téléphone : {contact_message.phone or '—'}\n\n"
                f"{contact_message.message}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient] if recipient else [],
            fail_silently=True,
        )

        messages.success(
            self.request,
            "Votre message a bien été envoyé. Nous revenons vers vous rapidement.",
        )
        return super().form_valid(form)
