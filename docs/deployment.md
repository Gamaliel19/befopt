# Déploiement — BEFOPT

## Choix de l'hébergement

### OPTION A — PaaS (Render, recommandé)

**Avantages** :
- Mise en ligne en quelques clics à partir du dépôt GitHub, sans gérer de serveur
- PostgreSQL managé (sauvegardes automatiques incluses)
- HTTPS/certificat automatique, pas de configuration Nginx à maintenir
- Adapté à une personne seule sans équipe DevOps dédiée

**Inconvénients** :
- Coût mensuel fixe même à faible trafic (environ 13 $/mois pour un service web « Starter » + une base PostgreSQL « Basic », hors bande passante/stockage — tarifs à vérifier sur render.com au moment de la souscription, ils évoluent)
- Moins de contrôle fin que sur un serveur dédié

### OPTION B — VPS (ex. Hetzner)

**Avantages** :
- Moins cher à ressources égales (VPS d'entrée de gamme autour de 5 $/mois)
- Contrôle total du serveur

**Inconvénients** :
- Demande de configurer et maintenir soi-même Nginx, Gunicorn (via systemd), PostgreSQL, les mises à jour de sécurité du système, les sauvegardes
- Plus de travail de maintenance dans la durée pour une seule personne

**RECOMMANDATION** : Render (Option A) pour le lancement — la simplicité l'emporte sur l'économie tant que le trafic reste modeste. Une migration vers un VPS reste possible plus tard si les coûts deviennent un frein, sans changement de code (le projet ne dépend d'aucune fonctionnalité propriétaire à Render).

---

## Prérequis avant déploiement

1. Le code doit être sur un dépôt Git (GitHub, GitLab...) — à votre charge, comme convenu
2. Un compte Render (render.com)
3. Un nom de domaine (si vous en achetez un — sinon Render fournit une adresse `*.onrender.com` gratuite pour démarrer)
4. Vos identifiants SMTP réels pour l'envoi d'e-mail (ex. : un compte Gmail avec mot de passe d'application, ou un service comme Brevo/SendGrid)

## Procédure (Render)

### 1. Base de données

Dans le tableau de bord Render : **New → PostgreSQL**. Notez l'URL de connexion interne générée (`DATABASE_URL`), déjà lue automatiquement par `config/settings/production.py`.

### 2. Service web

**New → Web Service**, connectez votre dépôt GitHub, puis renseignez :

| Champ              | Valeur                                                                                   |
|--------------------|------------------------------------------------------------------------------------------|
| Build Command      | `pip install -r requirements/production.txt && python manage.py collectstatic --noinput` |
| Start Command      | `gunicorn config.wsgi:application`                                                       |
| Pre-Deploy Command | `python manage.py migrate --noinput`                                                     |

### 3. Variables d'environnement

À définir dans l'onglet « Environment » du service (voir `.env.example` pour la liste complète) :

```
DJANGO_SECRET_KEY=<générée avec get_random_secret_key(), différente de celle du local>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=votre-domaine.td,befopt.onrender.com
DEFAULT_FROM_EMAIL=contact@befopt.td
CONTACT_RECIPIENT_EMAIL=deubarodrigue2018@gmail.com
EMAIL_HOST=...
EMAIL_PORT=587
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
EMAIL_USE_TLS=True
```

(`DATABASE_URL` est injectée automatiquement par Render, pas besoin de la définir vous-même.)

### 4. Premier déploiement

Render déploie automatiquement à chaque push sur la branche configurée. Une fois en ligne :

```
# Depuis le Shell Render (onglet "Shell" du service)
python manage.py createsuperuser
```

### 5. Nom de domaine

Dans l'onglet « Settings → Custom Domains » du service, ajoutez votre domaine et suivez les instructions DNS fournies (enregistrement CNAME ou A selon le cas). Le certificat HTTPS est généré automatiquement une fois le DNS propagé.

## Rollback

Render conserve l'historique des déploiements (onglet « Events ») : un bouton « Rollback » permet de revenir instantanément à une version précédente en cas de problème après une mise en ligne.

## Sauvegardes

La base PostgreSQL managée de Render inclut des sauvegardes automatiques quotidiennes (durée de rétention selon le plan choisi — à vérifier dans le tableau de bord). Pour une sauvegarde manuelle ponctuelle :

```
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```
