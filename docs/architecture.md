# Architecture — BEFOPT

## Vue d'ensemble

Application Django monolithique (pas de frontend séparé) : Django sert
à la fois les pages HTML (via Django Templates) et l'administration du
contenu (Django Admin). Aucune API REST/GraphQL n'existe — ce n'était
pas requis par le projet.

```
Navigateur
    │
    ▼
Django (Gunicorn)
    │
    ├── Templates (HTML) ── site public
    ├── Django Admin ────── CMS pour l'équipe BEFOPT
    └── PostgreSQL
```

## Apps

Chaque app a une responsabilité métier unique (section 7 du cahier des
charges initial) :

| App | Responsabilité |
|---|---|
| `apps.core` | `SiteSettings` (singleton), contexte global, sitemaps |
| `apps.pages` | Pages semi-statiques (À propos, Entreprises & Institutions), page d'accueil |
| `apps.services` | Les 4 domaines d'expertise |
| `apps.formations` | Fiches de formation |
| `apps.news` | Actualités |
| `apps.contact` | Formulaire de contact, messages reçus |

## Modèle de contenu

`Page`, `Service`, `Formation`, `NewsArticle` héritent tous de
`apps.core.models.PublishableModel` (abstrait) : slug auto-généré,
statut `draft`/`published`, champs SEO (`seo_title`,
`meta_description`, `og_image`), horodatage. Voir `docs/database.md`
pour le détail complet des champs.

Aucune relation par clé étrangère n'existe entre ces modèles — chacun
est autonome, aucun filtrage croisé n'était nécessaire au lancement.

## Flux d'une requête

1. `config/urls.py` route vers l'app correspondante par préfixe
   (`/expertises/`, `/formations/`, `/actualites/`, `/contact/`) —
   `apps.pages.urls` reste **volontairement en dernier**, car son motif
   générique `<slug:slug>/` intercepterait sinon les autres préfixes
2. La vue (`ListView`/`DetailView`/`FormView`) filtre sur
   `status=published` pour tout contenu public
3. Le `context_processor` de `apps.core` injecte `SiteSettings` dans
   chaque template, sans avoir à le repasser depuis chaque vue

## Design system

CSS dans `static/css/main.css`, entièrement en variables CSS
personnalisées (`:root`), dérivées du logo BEFOPT (rouge/gris/blanc).
Aucun framework CSS externe (Tailwind, Bootstrap...) — décision prise
en Phase 2 pour rester léger, conforme à la contrainte "éviter les
frameworks frontend lourds" du cahier des charges.

## Fichiers statiques et médias

- **STATIC** (`static/`) : CSS/JS du projet, servi via Whitenoise en
  production (compression + versionnage automatique)
- **MEDIA** (`media/`) : images uploadées via l'admin (formations,
  actualités, réglages du site), stockées sur le disque du service
  Render — voir la limitation notée dans `docs/maintenance.md`
