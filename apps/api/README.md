# 🚀 MSPR-API - Documentation pour les Nouveaux Contributeurs

[⬅️ Retour](/README.md)

Documentation rédigée par Samuel RESSIOT

---

## 📝 Introduction

Bienvenue dans le projet **MSPR-API** ! Ce document est conçu pour vous aider à comprendre rapidement l'architecture de l'application et à contribuer efficacement. Prenez le temps de lire cette documentation pour bien démarrer.

---

## Documentation OpenAPI

L'API est documentée automatiquement grâce à FastAPI. Vous pouvez accéder à la documentation interactive en utilisant l'URL suivante :
[http://localhost:8000/docs](http://localhost:8000/docs)

Ou si vous voulez mettre en place un swagger via le openapi.json, voici le fichier : [docs/openapi.json](docs/openapi.json)

---

## 🏗️ Vue d'Ensemble de l'Architecture

L'application est organisée en plusieurs couches pour garantir une séparation claire des responsabilités et faciliter la maintenance. Son architecture se base sur le principe de la **Clean Architecture**. Voici un aperçu des principales couches :

- **Couche Présentation** : Gère les requêtes HTTP et les réponses.
- **Couche Application** : Contient la logique métier et les cas d'utilisation.
- **Couche Domaine** : Définit les entités et les interfaces.
- **Couche Infrastructure** : Gère les interactions avec les systèmes externes (base de données, API, etc.).
- **Couche de Configuration** : Configure les dépendances et les paramètres globaux.
- **Couche de Tests** : Contient les tests unitaires et d'intégration.

📖 Consultez la fiche technique complète ici : [Clean Architecture](docs/architecture/architecture.md)

---

## 📂 Structure des Dossiers

Voici comment le projet est organisé :

```plaintext
apps/
├── api/
│   ├── src/
│   │   ├── app/
│   │   │   ├── continent/       # Module pour la gestion des continents
│   │   │   ├── country/         # Module pour la gestion des pays
│   │   │   ├── vaccine/         # Module pour la gestion des vaccins
│   │   ├── config/              # Configuration globale (injection de dépendances)
│   ├── docs/                    # Documentation du projet
```

- **`app/`** : Contient les modules métier.
- **`config/`** : Configure les dépendances et les paramètres globaux.
- **`docs/`** : Documentation pour les contributeurs.

---

## 📜 Cycle de Vie d'une Requête API

Découvrez le cycle de vie complet d'une requête API, de l'envoi de la requête par l'utilisateur jusqu'à la réponse renvoyée par le système :

📖 [Cycle de Vie d'une Requête API](docs/uml/sequences/api_request/life_cycle_api_request.md)

---

## 📘 Diagramme de Classe - Module Country

Pour une vue détaillée du fonctionnement du module **Country**, consultez le diagramme de classe dédié. Ce document explique les principales classes, leurs responsabilités, et leurs relations.

📖 [Diagramme de Classe - Module Country](docs/uml/classes/country/country_class_diagram.md)

---

## 📊 Diagramme de Séquence - AddCountryUseCase

Le diagramme de séquence **AddCountryUseCase** illustre le processus métier pour ajouter un nouveau pays dans le système. Il montre les interactions entre les différentes couches de l'application, notamment la validation des données, la vérification de l'existence du pays et du continent, ainsi que la création ou la réactivation du pays.

📖 [Diagramme de Séquence - AddCountryUseCase](docs/uml/sequences/add_country_usecase/add_country_usecase.md)

---

## 🗄️ Migrations de la Base de Données

Les migrations de la base de données sont gérées par **Alembic**, un outil puissant de migration pour SQLAlchemy.

### Principes de Base

Les migrations permettent de :

- Versionner les changements de schéma de base de données
- Effectuer des mises à jour sans perte de données
- Revenir à une version précédente du schéma si nécessaire

### Bonnes Pratiques

1. **Créez des messages descriptifs** pour vos migrations afin de facilement identifier leur but.
2. **Vérifiez toujours les fichiers de migration générés** avant de les appliquer pour éviter les erreurs.
3. **Testez les migrations** sur un environnement de développement avant de les appliquer en production.
4. **Ne modifiez jamais une migration déjà appliquée** sur d'autres environnements.

Pour plus d'informations, consultez la [documentation des migrations](docs/migrations/migrations.md).

---

## 🤝 Comment Contribuer

### 1️⃣ **Cloner le Projet**

Commencez par cloner le dépôt Git :

```bash
git clone https://github.com/Sam-rst/EPSI_B3_MSPR-Groupe_MATS.git
cd EPSI_B3_MSPR-Groupe_MATS
```

### 2️⃣ **Configurer l'Environnement**

Créez un fichier `.env` à la racine du projet avec les variables d'environnement nécessaires. Vous pouvez utiliser le fichier d'exemple fourni :

```bash
cp config/env/dev.conf .env
```

### 3️⃣ **Lancer le Projet**

Utilisez Docker pour démarrer l'application :

```bash
docker-compose up --build -d
```

### 4️⃣ **Tester vos Modifications**

Avant de soumettre vos modifications, assurez-vous que tous les tests passent :

```bash
python -m unittest discover -f tests -v
```

---

## 📚 Ressources Utiles

- [📘 Documentation FastAPI](https://fastapi.tiangolo.com/)
- [📘 Documentation SQLAlchemy](https://www.sqlalchemy.org/)
- [📘 Documentation Alembic](https://alembic.sqlalchemy.org/)

---

## ❓ Questions Fréquentes

### ❔ **Comment ajouter une nouvelle fonctionnalité ?**

1. Créez un nouveau module dans `app/`.
2. Ajoutez les fichiers nécessaires : contrôleurs, use cases, repositories.
3. Configurez les dépendances dans `container.py`.

### ❔ **Comment exécuter les migrations de base de données ?**

Utilisez Alembic pour générer et appliquer les migrations :

```bash
alembic revision --autogenerate -m "Description de la migration"
alembic upgrade head
```

---

## 🎉 Conclusion

Nous sommes ravis de vous accueillir dans ce projet ! Si vous avez des questions ou des suggestions, n'hésitez pas à les partager avec l'équipe. Bonne contribution et bon développement ! 🚀
