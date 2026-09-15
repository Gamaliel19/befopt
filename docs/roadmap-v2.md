# Roadmap V2 — BEFOPT

Fonctionnalités identifiées mais volontairement reportées faute de
contenu réel ou de besoin confirmé au moment du lancement (voir
Phase 1 du projet). Aucune n'est urgente ; à prioriser selon les
besoins réels de BEFOPT une fois le site en usage.

## Contenu en attente de matière

- **Témoignages** : modèle simple à ajouter (`Testimonial` : nom,
  fonction, citation, éventuelle photo) dès que BEFOPT dispose de
  témoignages réels à publier
- **Partenaires** : modèle `Partner` (nom, logo, lien) dès qu'ils sont
  officiellement communiqués
- **Chiffres clés / statistiques** : à intégrer sur la page d'accueil
  ou "À propos" si BEFOPT souhaite les communiquer un jour

## Fonctionnalités

- **Multilingue** (FR/EN) : pertinent vu la dimension internationale
  du cabinet — `django-modeltranslation` ou équivalent
- **Prise de rendez-vous / demande de devis structurée** : formulaire
  dédié au-delà du contact générique actuel
- **Plateforme de cours en ligne** (mentionnée dans la vision du
  dépliant) : projet à part entière, hors périmètre d'un site vitrine,
  à cadrer séparément le moment venu
- **FAQ** : modèle simple si des questions récurrentes émergent
- **Newsletter** : capture d'e-mail + envoi, si BEFOPT souhaite
  communiquer régulièrement

## Technique

- **Stockage média externe** (voir `docs/maintenance.md`) — à traiter
  en priorité, avant les autres points de cette liste
- **Monitoring** (Sentry ou équivalent) si le trafic augmente
- **CSP (Content-Security-Policy)** une fois le site stabilisé
