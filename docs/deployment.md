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

Dans le tableau de bord Render : **New → PostgreSQL**. Une fois créée, ouvrez la fiche de cette base et copiez la valeur **Internal Database URL**.

**Important — cette liaison n'est pas automatique.** Contrairement à ce que j'avais indiqué précédemment, Render ne relie pas tout seul une base PostgreSQL à un service web : il faut ajouter manuellement `DATABASE_URL` dans les variables d'environnement du service web (étape 3), avec la valeur copiée ici.

### 2. Service web

**New → Web Service**, connectez votre dépôt GitHub, puis renseignez :

| Champ | Valeur |
|---|---|
| Build Command | `pip install -r requirements/production.txt && python manage.py collectstatic --noinput` |
| Start Command | `python manage.py migrate --noinput && (python manage.py createsuperuser --noinput \|\| true) && gunicorn config.wsgi:application` |

**Note sur la Pre-Deploy Command** : cette fonctionnalité (recommandée dans une version précédente de ce document) est réservée aux plans payants de Render — sur un plan gratuit/starter, le champ reste grisé. La solution ci-dessus contourne ce blocage en exécutant `migrate` directement au démarrage, avant Gunicorn : la commande est sans risque à chaque redémarrage (Django ignore les migrations déjà appliquées).

**Créer le compte administrateur sans accès au Shell** : si l'onglet Shell est lui aussi indisponible sur votre plan, la Start Command inclut déjà `createsuperuser --noinput`, qui lit les identifiants depuis trois variables d'environnement à ajouter (section 3 ci-dessous) :

```
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@befopt.td
DJANGO_SUPERUSER_PASSWORD=<un mot de passe robuste, différent de celui de votre compte Render>
```

Le `|| true` rend l'étape silencieuse et sans effet une fois le compte déjà créé (testé : les redémarrages suivants ne provoquent ni erreur ni doublon). Une fois connecté à `/admin/` avec ce compte, vous pouvez retirer `DJANGO_SUPERUSER_PASSWORD` des variables d'environnement si vous préférez ne pas le laisser en clair dans la configuration.

### 3. Variables d'environnement

À définir dans l'onglet « Environment » du service (voir `.env.example` pour la liste complète) :

```
DJANGO_SETTINGS_MODULE=config.settings.production
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

**Important — `DJANGO_SETTINGS_MODULE` est indispensable.** `manage.py` pointe par défaut vers `config.settings.development` (pratique en local). Sans cette variable définie sur Render, le build essaie de charger les réglages de développement, qui exigent quand même `DJANGO_SECRET_KEY` — d'où l'erreur `decouple.UndefinedValueError: DJANGO_SECRET_KEY not found` si les variables ne sont pas encore renseignées au moment du build.

`DATABASE_URL` n'est **pas** injectée automatiquement (voir étape 1 ci-dessus) — ajoutez-la vous-même dans cette même liste, avec la valeur copiée depuis la fiche de votre base PostgreSQL.

**Version de Python** : Render lit un fichier `.python-version` à la racine du projet (déjà présent, fixé à `3.12.8`) — pas `runtime.txt`, qui est une convention Heroku ignorée par Render.

## Dépannage — erreur 500 après un déploiement réussi

Si le build et le déploiement se terminent avec succès mais que le site renvoie une erreur 500 sur toutes les pages, c'est presque toujours l'une de ces deux causes (avant de chercher plus loin, consultez l'onglet **Logs** du service sur Render : la trace Python complète y est écrite même quand `DEBUG=False`) :

1. **`DATABASE_URL` absente ou mal renseignée** → l'application ne peut pas se connecter à la base. Vérifiez qu'elle est bien présente dans Environment, avec la valeur exacte de l'*Internal Database URL* de votre base PostgreSQL.
2. **Migrations jamais appliquées** → la base existe mais ne contient aucune table. Vérifiez que la Start Command du service est bien celle indiquée à l'étape 2 (avec `migrate --noinput` en premier), pas juste `gunicorn config.wsgi:application` seul.

Après correction, redéclenchez un déploiement (« Manual Deploy → Deploy latest commit »).

### 4. Premier déploiement

Render déploie automatiquement à chaque push sur la branche configurée. Le compte administrateur est créé automatiquement au premier démarrage grâce aux variables `DJANGO_SUPERUSER_*` (étape 2). Si l'onglet **Shell** est disponible sur votre plan, vous pouvez aussi créer/gérer des comptes manuellement :

```
# Depuis le Shell Render (onglet "Shell" du service, si disponible sur votre plan)
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
