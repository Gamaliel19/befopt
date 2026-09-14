# BEFOPT — site web professionnel

Site vitrine du cabinet BEFOPT, développé en Django monolithique
(Django Templates + PostgreSQL), administrable entièrement depuis
Django Admin.

## État du projet

Squelette, modèles, admin CMS, frontend, SEO et tests sont en place
(Phases 4 à 10). Configuration de production prête (Phase 11) — voir
`docs/deployment.md` pour la procédure de mise en ligne.

## Stack

- Python 3.12 ou 3.13
- Django 5.2 (LTS)
- PostgreSQL 16+
- Django Templates, HTML5, CSS3, JS vanilla (pas de framework frontend)

## Installation (Windows)

### 1. Prérequis

- Python 3.12 ou 3.13 installé ([python.org](https://www.python.org/downloads/), cocher "Add Python to PATH")
- PostgreSQL 16+ installé ([postgresql.org](https://www.postgresql.org/download/windows/))
- Git

### 2. Environnement virtuel

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements\development.txt
```

### 3. Variables d'environnement

Copiez `.env.example` en `.env` et renseignez vos valeurs (clé secrète,
identifiants PostgreSQL locaux).

### 4. Base de données

Créez la base et l'utilisateur PostgreSQL (via pgAdmin ou `psql`) avec
les identifiants renseignés dans `.env`, puis :

```
python manage.py migrate
python manage.py createsuperuser
```

### 5. Lancer le serveur

```
python manage.py runserver
```

Le site est accessible sur http://127.0.0.1:8000/ et l'admin sur
http://127.0.0.1:8000/admin/.

## Structure du projet

```
befopt/
├── config/settings/{base,development,production}.py
├── apps/{core,pages,services,formations,news,contact}/
├── templates/
├── static/
├── media/
├── requirements/{base,development,production}.txt
└── docs/
```

Voir `docs/architecture.md` (à venir) pour le détail de chaque app.

## Documentation

- `docs/development.md` — prise en main développeur
- `docs/database.md` — modèle de données
- `docs/admin.md` — guide d'utilisation de Django Admin pour l'équipe BEFOPT
- `docs/deployment.md` — mise en production
- `docs/security.md` — pratiques de sécurité appliquées
- `docs/maintenance.md` — procédures de maintenance

(Ces documents seront rédigés au fil des phases correspondantes de la
roadmap, et non tous d'un coup.)
