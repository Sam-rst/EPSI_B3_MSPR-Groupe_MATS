# API Rest

## Introduction

Cette documentation décrit l'API Rest du projet EPSI_MSPR_B3-Groupe_MATS. Elle couvre les conventions de nommage, le fonctionnement, l'architecture, et d'autres aspects essentiels.

## Conventions de Nommage

- **Méthodes et Fonctions** : Utilisez des noms en minuscules avec des underscores, par exemple, `get_user`.
- **Classes** : Utilisez le PascalCase, par exemple, `UserEntity`.
- **Variables** : Utilisez des noms en minuscules avec des underscores, par exemple, `user_id`.

## Fonctionnement

L'API est construite avec FastAPI et suit les principes RESTful. Elle permet de gérer les entités de continent avec des opérations CRUD (Create, Read, Update, Delete).

## Architecture

- **Domaine** : Contient les entités et la logique métier.
- **Infrastructure** : Gère la persistance des données et les interactions avec la base de données.
- **Présentation** : Gère les routes et les réponses HTTP.

## Lancement

Utilisez Docker pour lancer l'API (ATTENTION : bien être à la racine du projet):

```bash
# Si ce n'est pas déjà exécuté :
docker-compose up --build -d

# Pour regarder les logs :
docker-compose logs -f MSPR-API

# Pour rentrer dans le container via un terminal (utile pour exécuter des commandes telles que alembic pour les migrations) :
docker exec -it MSPR-API /bin/bash
```

## Migrations

### Configuration de la base de données

Pour les nouveaux arrivants, voici comment configurer et gérer la base de données du projet :

1. **Configuration initiale** :

   ```bash
   # Accéder au container de l'API
   docker exec -it MSPR-API /bin/bash
   
   # Initialiser Alembic (si ce n'est pas déjà fait)
   alembic init migrations
   ```

2. **Commandes principales pour les migrations** :

   ```bash
   # Créer une nouvelle migration
   alembic revision --autogenerate -m "Description de la migration"
   
   # Appliquer toutes les migrations en attente
   alembic upgrade head
   
   # Revenir en arrière d'une migration
   alembic downgrade -1
   
   # Voir le statut des migrations
   alembic current
   ```

Pour plus d'informations, consultez la documentation détaillée sur les migrations : [en savoir +](docs/migrations.md)
