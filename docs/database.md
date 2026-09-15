# Base de données — BEFOPT

PostgreSQL en production et en local. Aucune relation par clé
étrangère entre les 6 modèles — schéma volontairement plat (voir
Phase 3/5 de la roadmap pour la justification).

## SiteSettings (singleton — `apps.core`)

Un seul enregistrement, chargé via `SiteSettings.load()`.

| Champ | Type | Notes |
|---|---|---|
| site_name | CharField | |
| tagline | CharField | Slogan |
| mission_text | TextField | |
| phone_1, phone_2 | CharField | |
| email | EmailField | |
| address, bp | CharField | |
| facebook_url, linkedin_url, twitter_url | URLField | Vides tant que non fournis |
| footer_text | CharField | |
| default_seo_title, default_meta_description | CharField | Repli SEO |
| default_og_image | ImageField | Repli partage social |

## Socle commun — `PublishableModel` (abstrait, `apps.core`)

Hérité par `Page`, `Service`, `Formation`, `NewsArticle` :

| Champ | Type | Notes |
|---|---|---|
| slug | SlugField (unique) | Auto-généré depuis `title` si vide |
| status | CharField (choix) | `draft` / `published` |
| seo_title | CharField | |
| meta_description | CharField | |
| og_image | ImageField | |
| created_at, updated_at | DateTimeField | Automatiques |

## Page (`apps.pages`)

`title`, `content` (TextField), + socle commun.

## Service (`apps.services`)

`title`, `short_description`, `content`, `icon`, `order`
(PositiveIntegerField, contrôle l'affichage), + socle commun.

## Formation (`apps.formations`)

`title`, `description`, `content`, `image`, `image_alt_text`
(obligatoire si `image` renseignée — validé par `clean()`),
`published_at`, + socle commun.

## NewsArticle (`apps.news`)

`title`, `excerpt`, `content`, `image`, `image_alt_text` (même règle
que Formation), `published_at`, + socle commun.

## ContactMessage (`apps.contact`)

Pas de socle commun (pas de contenu publiable) :

| Champ | Type | Notes |
|---|---|---|
| name, email, phone, subject | CharField/EmailField | |
| message | TextField | |
| status | CharField (choix) | `new` / `processed` |
| created_at | DateTimeField | Automatique |

## Migrations

```
python manage.py makemigrations   # après toute modification de modèle
python manage.py migrate
```

En production, la migration s'exécute automatiquement au démarrage
(voir Start Command dans `docs/deployment.md`) — jamais besoin de la
lancer manuellement après un déploiement normal.
