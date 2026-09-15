# Maintenance — BEFOPT

## ⚠️ Point important à corriger rapidement : stockage des images

Le service web Render actuellement utilisé n'a **pas de disque
persistant configuré**. Concrètement : toute image uploadée depuis
l'admin (logo, image de formation, image d'actualité...) est stockée
sur le disque du service, et **sera perdue au prochain déploiement ou
redémarrage** (mise à jour du code, redémarrage automatique après
inactivité selon le plan, etc.).

Ce n'était pas visible pendant les tests (Phases 4 à 10, en local avec
PostgreSQL/SQLite de test) et n'empêche pas le site de fonctionner
aujourd'hui — mais toute image que l'équipe BEFOPT ajoute maintenant
risque de disparaître sans prévenir.

**Deux solutions, à traiter avant d'ajouter des images définitives :**

1. **Disque persistant Render** (« Persistent Disk », fonctionnalité
   payante selon le plan) : le plus simple, mais dépend du plan
   souscrit — à vérifier dans le tableau de bord Render
2. **Stockage objet externe** (ex. Cloudflare R2, Backblaze B2,
   Cloudinary) via `django-storages` : plus de travail d'intégration,
   mais fonctionne sur n'importe quel plan et n'importe quel hébergeur

Je recommande d'en discuter avant que l'équipe BEFOPT ne commence à
publier des formations/actualités avec images.

## Mises à jour de dépendances

Trimestriellement (ou après une alerte de sécurité connue) :

```
pip list --outdated
```

Mettre à jour une dépendance à la fois, relancer `python manage.py test`
après chaque mise à jour avant de déployer.

## Sauvegardes

La base PostgreSQL managée de Render inclut des sauvegardes
automatiques (fréquence selon le plan — à vérifier dans le tableau de
bord). Sauvegarde manuelle ponctuelle :

```
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

## Surveillance

Onglet **Logs** du service Render pour tout diagnostic (erreurs 500,
échecs de build). Aucun outil de monitoring externe (Sentry, etc.)
n'est configuré au lancement — à envisager si le trafic augmente.

## Rollback

Voir `docs/deployment.md`, section « Rollback » — un déploiement
précédent peut être restauré en un clic depuis l'onglet **Events** du
service.

## Contacts techniques

Ce projet a été développé par Gamaliel. Pour toute reprise par un
autre développeur, `docs/architecture.md` et `docs/development.md`
couvrent la structure du projet et les conventions utilisées.
