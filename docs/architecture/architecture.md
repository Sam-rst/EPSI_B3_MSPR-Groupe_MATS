# 🌐 Architecture du Projet

[⬅️ Retour](/README.md)

Documentation rédigée par Samuel RESSIOT

---

Bienvenue dans la documentation de l'architecture globale de notre solution. Ce document a pour objectif de fournir une vue d'ensemble claire et détaillée du fonctionnement de notre système, afin de faciliter l'intégration des nouveaux arrivants.

---

## 📝 Introduction

Notre solution est conçue pour répondre aux besoins de gestion des données, de visualisation et d'interaction avec des utilisateurs finaux. Elle repose sur une architecture modulaire et évolutive, intégrant plusieurs composants interconnectés.

---

## 🏗️ Vue d'Ensemble

L'architecture est organisée autour des principaux composants suivants :

- **API Rest** : Fournit des endpoints pour interagir avec les données.
- **ETL** : Gère l'extraction, la transformation et le chargement des données dans la base de données.
- **Base de Données PostgreSQL** : Stocke les données de manière structurée.
- **Metabase** : Permet la visualisation des données pour les utilisateurs finaux.
- **Interface ETL** : Permet aux développeurs de déclencher des pipelines ETL.

---

## 📊 Diagramme d'Architecture

Voici une représentation visuelle de l'architecture globale de notre solution :

![Diagramme d'Architecture](img/architecture.svg)

---

## 🧩 Composants

### 1️⃣ **API Rest**

- **Rôle** : Fournir une interface pour interagir avec les données via des requêtes HTTP.
- **Technologie** : FastAPI.
- **Fonctionnalités** :
  - CRUD (Create, Read, Update, Delete) sur les entités.
  - Authentification (à venir).

### 2️⃣ **ETL**

- **Rôle** : Extraire, transformer et charger les données dans la base de données.
- **Technologie** : Python (pandas, Airflow).
- **Fonctionnalités** :
  - Nettoyage des données.
  - Agrégation et enrichissement des données.

### 3️⃣ **Base de Données PostgreSQL**

- **Rôle** : Stocker les données de manière fiable et performante.
- **Technologie** : PostgreSQL.
- **Fonctionnalités** :
  - Stockage relationnel.
  - Support des transactions.

### 4️⃣ **Metabase**

- **Rôle** : Fournir des tableaux de bord et des visualisations interactives.
- **Technologie** : Metabase.
- **Fonctionnalités** :
  - Visualisation des données.
  - Création de rapports personnalisés.

### 5️⃣ **Interface ETL**

- **Rôle** : Permettre aux développeurs de déclencher des pipelines ETL.
- **Technologie** : Interface CLI ou API.
- **Fonctionnalités** :
  - Déclenchement manuel des pipelines.
  - Monitoring des exécutions.

---

## 🔄 Flux de Données

### Étapes principales

1. **Extraction** : Les données sont collectées depuis des sources externes via l'ETL.
2. **Transformation** : Les données sont nettoyées et enrichies avant d'être chargées.
3. **Chargement** : Les données transformées sont insérées dans la base de données PostgreSQL.
4. **Interaction API** : Les utilisateurs interagissent avec les données via l'API Rest.
5. **Visualisation** : Les utilisateurs finaux accèdent aux tableaux de bord via Metabase.

---

## 🛠️ Technologies Utilisées

- **FastAPI** : Framework pour l'API Rest.
- **PostgreSQL** : Base de données relationnelle.
- **Metabase** : Outil de visualisation des données.
- **Docker** : Conteneurisation des services.
- **Airflow** : Orchestration des pipelines ETL.

---

## 📂 Structure du Projet

Voici une vue d'ensemble de la structure des dossiers du projet :

```plaintext
📦 Mon-Projet 
├── 📂 apps
│   ├── 📂 api             # API REST principale (FastAPI)
│   ├── 📂 etl             # Pipeline ETL (Airflow + pandas)  
│   ├── 📂 frontend        # Web App (Next.js)
│   ├── 📂 monitoring      # Logs & Stats (Prometheus, Grafana, Loki)
│
├── 📂 infra
│   ├── 📂 db              # PostgreSQL
│   ├── 📂 docker          # Fichiers Docker
│
├── docker-compose.yml     # Configuration des services
```

---

## 🌟 Points Forts de l'Architecture

- **Modularité** : Chaque composant est indépendant, ce qui facilite la maintenance et l'évolution.
- **Scalabilité** : Les services peuvent être mis à l'échelle individuellement.
- **Interopérabilité** : Les composants communiquent via des interfaces standardisées.

---

## 🎉 Conclusion

Cette architecture est conçue pour être robuste, évolutive et facile à maintenir. Si vous avez des questions ou des suggestions, n'hésitez pas à les partager avec l'équipe. Bienvenue à bord ! 🚀
