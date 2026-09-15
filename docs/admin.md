# Guide d'utilisation — Administration du site BEFOPT

Ce guide s'adresse à l'équipe BEFOPT, sans connaissance technique
requise.

## Se connecter

Allez sur `https://votre-domaine/admin/` (ou `https://befopt.onrender.com/admin/`
en attendant un nom de domaine dédié) et connectez-vous avec le compte
administrateur créé lors de la mise en ligne.

## Modifier les informations générales du site

Menu **Réglages du site** : nom du site, slogan, texte de mission,
téléphones, e-mail, adresse, réseaux sociaux. Ces informations
apparaissent dans l'en-tête et le pied de page de **toutes** les
pages du site — un seul endroit à modifier.

- Laissez un champ de réseau social vide si BEFOPT ne l'utilise pas :
  le lien n'apparaîtra tout simplement pas sur le site
- Cliquez sur **Enregistrer** en bas de la page pour appliquer les
  changements

## Modifier une page (À propos, Entreprises & Institutions)

Menu **Pages** → cliquez sur la page à modifier. Le champ **Statut**
doit être sur **Publié** pour que la page soit visible par les
visiteurs ; **Brouillon** la rend invisible sans la supprimer.

## Gérer les services (nos 4 expertises)

Menu **Services / Expertises**. Depuis la liste, vous pouvez changer
l'**ordre d'affichage** et le **statut** directement, sans ouvrir
chaque fiche (cliquez sur le champ dans le tableau, modifiez, puis
**Enregistrer** en bas de la liste).

## Publier une formation ou une actualité

Menus **Formations** / **Actualités** → **Ajouter**. Remplissez :

- **Titre** (le slug/adresse de la page se génère automatiquement)
- **Description courte** (Formations) ou **Chapô/résumé** (Actualités) : affiché dans la liste
- **Contenu détaillé** : affiché sur la fiche complète
- **Image** (optionnelle) : si vous en ajoutez une, le champ **Texte
  alternatif de l'image** devient obligatoire (décrivez l'image en
  une phrase — c'est utilisé par les lecteurs d'écran pour les
  personnes malvoyantes)
- **Statut** : passez sur **Publié** quand le contenu est prêt

Tant qu'aucune formation/actualité n'est publiée, le site affiche un
message "Aucune formation/actualité publiée pour le moment" plutôt
qu'une page vide — c'est normal et voulu.

## Consulter les messages reçus via le formulaire de contact

Menu **Messages de contact**. Chaque message reçu apparaît
automatiquement (une notification est aussi envoyée par e-mail).
Vous ne pouvez pas modifier le contenu d'un message (c'est volontaire,
pour préserver ce que le visiteur a réellement écrit), mais vous
pouvez changer son statut en **Traité** une fois qu'il a été géré —
ou sélectionner plusieurs messages et utiliser l'action groupée
"Marquer comme traités" en haut de la liste.

## Bon à savoir

- Une fiche en **Brouillon** n'est jamais visible sur le site public,
  même en connaissant son adresse directe
- Les images ajoutées via l'admin sont actuellement stockées sur le
  serveur — voir `docs/maintenance.md` pour une limitation importante
  à ce sujet, à corriger avant d'y stocker du contenu définitif
