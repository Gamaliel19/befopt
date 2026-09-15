# Sécurité — BEFOPT

Récapitulatif des pratiques appliquées (section 20 du cahier des
charges initial), pour référence et audit futur.

## Configuration

- `DEBUG = False` en production (`config/settings/production.py`) —
  aucune trace d'erreur détaillée n'est exposée aux visiteurs
- `SECRET_KEY` et tous les identifiants (base de données, SMTP) lus
  depuis les variables d'environnement, jamais codés en dur
- `ALLOWED_HOSTS` explicite (pas de wildcard `*`)
- `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` :
  tout le trafic est forcé en HTTPS, cookies transmis uniquement en
  HTTPS
- `SECURE_HSTS_SECONDS` (1 an) + `SECURE_HSTS_INCLUDE_SUBDOMAINS` +
  `SECURE_HSTS_PRELOAD` : empêche un navigateur de revenir en HTTP
  même sur une requête ultérieure
- `X_FRAME_OPTIONS = "DENY"` : empêche l'affichage du site dans une
  iframe (protection anti-clickjacking)

## Application

- **CSRF** : activé par défaut sur tous les formulaires Django
  (`{% csrf_token %}`), **testé** : une requête POST sans jeton CSRF
  vers le formulaire de contact renvoie bien une erreur 403
- **Formulaire de contact** : protection anti-spam par champ honeypot
  (invisible pour un humain, souvent rempli par un robot — la
  soumission est alors rejetée sans rien enregistrer), validation
  serveur sur tous les champs (e-mail, champs requis)
- **Admin** : accès réservé aux comptes `is_staff`, testé (un
  utilisateur non-staff ne voit aucun modèle) ; contenu d'un message
  de contact toujours en lecture seule pour éviter qu'un
  administrateur altère ce qu'un visiteur a réellement écrit
- **Validation d'accessibilité** : une image sans texte alternatif est
  rejetée à l'enregistrement (Formation, Actualité)

## Dépendances

`requirements/*.txt` épingle des plages de version (ex.
`Django>=5.2,<5.3`) plutôt que des versions figées strictement, pour
recevoir les correctifs de sécurité mineurs sans changement de
version majeure non testé.

## Recommandations pour la suite

- Mettre en place une politique de mise à jour régulière des
  dépendances (`pip list --outdated`), au minimum trimestrielle
- Envisager un `Content-Security-Policy` (CSP) une fois le site
  stabilisé, non mis en place au lancement pour ne pas bloquer les
  polices Google Fonts et scripts futurs sans réglage fin préalable
- Voir `docs/maintenance.md` pour la question du stockage des médias
  en production, qui a aussi une dimension "perte de données" au-delà
  de la sécurité
