# Guide développeur — BEFOPT

## Prise en main

Voir `README.md` pour l'installation complète (Windows). En résumé :

```
venv\Scripts\activate
pip install -r requirements\development.txt
python manage.py migrate
python manage.py runserver
```

## Conventions de code

- **PEP 8**, appliqué via `ruff` (`ruff check .`) et `black`
  (`black .`) — tous deux dans `requirements/development.txt`
- Un modèle par fichier logique, pas de vue "fourre-tout" : chaque app
  a ses propres `models.py`/`views.py`/`urls.py`/`admin.py`
- Les modèles publiables héritent de `PublishableModel`
  (`apps.core.models`) plutôt que de dupliquer slug/statut/SEO
- Commentaires en français, alignés sur la langue du projet et de
  l'équipe BEFOPT

## Git

Conventional Commits recommandés (section 24 du cahier des charges
initial) :

```
feat: ajoute la pagination sur la liste des actualités
fix: corrige l'ordre des URLs qui interceptait /expertises/
docs: met à jour le guide de déploiement
```

## Tests

```
python manage.py test
```

31 tests actuellement (voir `docs/architecture.md` pour la
répartition par app). Tout ajout de fonctionnalité touchant à la
visibilité brouillon/publié, à la validation d'un formulaire ou à la
sécurité doit s'accompagner d'un test.

## Environnements

| Environnement | Fichier de settings | Base de données |
|---|---|---|
| Local (votre machine) | `config.settings.development` (par défaut) | PostgreSQL local |
| Production (Render) | `config.settings.production` (variable `DJANGO_SETTINGS_MODULE`) | PostgreSQL managé Render |

## Ajouter un nouveau type de contenu

Pour un futur modèle publiable (ex. Témoignages, Partenaires — voir la
roadmap V2), suivre le patron déjà en place :

1. Créer l'app (`python manage.py startapp <nom>` dans `apps/`, puis
   corriger `name = "apps.<nom>"` dans `apps.py`, comme pour les apps existantes)
2. Modèle héritant de `PublishableModel`
3. `admin.py` avec `list_display`, `list_filter`, `search_fields`,
   `prepopulated_fields = {"slug": ("title",)}`
4. Vues `ListView`/`DetailView` filtrant sur `status=published`
5. Templates suivant la structure de `templates/formations/` (y
   compris l'état vide)
6. Ajouter l'app à `LOCAL_APPS` (`config/settings/base.py`) et son
   sitemap dans `apps/core/sitemaps.py`
