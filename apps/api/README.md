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
docker-compose up --build -d
```

## Endpoints Principaux

- `GET /continents` : Récupère tous les continents.
- `POST /continents` : Crée un nouveau continent.
- `PUT /continents/{id}` : Met à jour un continent existant.
- `DELETE /continents/{id}` : Supprime un continent.
