# EPSI B3 MSPRs

Voici le repository de notre groupe pour les MSPRs de la formation EPSI B3 en DEVIA et Data Science (Fullstack + DevOps).

Contributeurs :

1. Samuel RESSIOT
2. Tom WILK-RAVOUX
3. Alexandre PIERRE
4. Maxime DUSSORT

---
## **Navigation dans la Documentation**
- ➡️ Documentation IA (W.I.P)
- ➡️ Documentation UML (W.I.P)
- [➡️ Documentation Merise](docs/diagrams/merise/merise.md)
- [➡️ Documentation Architecture](docs/architecture/architecture.md)




## **📜 Architecture logicielle du projet**  

### **Explication**

- **Docker (compose)** : Encapsule l'infrastructure logicielle.
- **API Gateway (Backend)** : Contient l'ETL et l'API REST, qui communiquent avec la base PostgreSQL.
- **Metabase** : Outil de visualisation de données connecté à PostgreSQL.
- **Client** : Interagit avec Metabase.
- **Développeur** : Accède aux services via authentification (Auth).

### **Schéma :**

```mermaid
graph TD;
    subgraph "ENVIRONNEMENT"
        subgraph "Docker (compose) - All services"
            direction TB
            subgraph "API Gateway - Backend"
                ETL["ETL"] --> |Write| DB["PostgreSQL"]
                API -->|CRUD| DB["PostgreSQL"]
                DB -->|Receive| API["API Rest"]
            end

            Metabase["Metabase (dataviz)"] -->|Read| DB
        end

        Dev["Developer"] -- HTTP (Auth) --> API
        Dev -- HTTP (Auth) --> ETL
        Dev -- Connexion - HOST --> DB
        Client["Client"] --> Metabase
    end
```

## **📜 Liste des technologies du projet**  

### **1️⃣ Backend (API REST FastAPI pour le CRUD)**  

| Technologie | Version | Raison du choix | Usage |
|-------------|---------|-----------------|-------|
| **FastAPI** | Latest | Performant, async natif, doc automatique | API REST |
| **Python** | 3.11+ | Langage flexible et puissant | Dev de l'API et de l'IA |
| **SQLAlchemy** | Latest | ORM puissant et compatible avec PostgreSQL | Gestion de la base de données |
| **Pydantic** | Latest | Validation et sérialisation des données | Modèles de données |
| **Celery** | Latest | Gestion des tâches asynchrones | Traitements en arrière-plan |
| **Redis** | Latest | Caching et gestion des files de tâches | Optimisation des performances |
| **PostgreSQL** | 15+ | Performant et robuste pour les données relationnelles | Base de données principale |
| **Docker** | Latest | Conteneurisation pour déploiement | Exécution en environnement isolé |
| **Gunicorn / Uvicorn** | Latest | Serveur WSGI/ASGI performant | Déploiement de l'API |
| **OAuth2 / JWT / Keyclock** | Latest | Sécurité et authentification | Gestion des utilisateurs et des permissions |

---

### **2️⃣ Frontend (Application NextJS)**  

| Technologie | Version | Raison du choix | Usage |
|-------------|---------|-----------------|-------|
| **Next** | Latest | Framework robuste et maintenable | Développement du frontend / API |
| **TypeScript** | Latest | Typage fort, maintenabilité | Langage principal |
| **TailwindCSS** | Latest | Styling moderne et flexible | UI et mise en page |
| **NGXS ou Redux** | Latest | Gestion centralisée du state | State management |
| **Metabase** | Latest | Open source | Data visualisation |

---

### **3️⃣ ETL (Traitement et nettoyage des données en FastAPI)**  

| Technologie | Version | Raison du choix | Usage |
|-------------|---------|-----------------|-------|
| **FastAPI** | Latest | Orchestration des workflows ETL | Planification des tâches |
| **Pandas** | Latest | Manipulation des données | Nettoyage et transformation des données |
| **DuckDB** | Latest | Traitement performant des datasets volumineux | Analyse et transformation |
| **TKinter**| Latest | Bibliothèque standard pour les interfaces graphiques en Python | Interface graphique et la sélection de fichiers |
| **SQLAlchemy** | Latest | ORM pour interagir avec les bases | Stockage des données |

---

### **4️⃣ Infrastructure & DevOps**  

| Technologie | Version | Raison du choix | Usage |
|-------------|---------|-----------------|-------|
| **Docker** | Latest | Conteneurisation | Isolation et portabilité |
| **Docker Compose** | Latest | Gestion multi-conteneurs | Environnements Dev & Prod |
| **Kubernetes (K8s)** | Optional | Scalabilité et orchestration | Gestion des déploiements |
| **Terraform** | Latest | Infrastructure as Code | Automatisation du déploiement |
| **Ansible** | Latest | Configuration automatisée | Provisioning des serveurs |
| **NGINX / Traefik** | Latest | Proxy et Load Balancer | Redirection et gestion des requêtes |

---

### **5️⃣ Observabilité et Monitoring**  

| Technologie | Version | Raison du choix | Usage |
|-------------|---------|-----------------|-------|
| **Prometheus** | Latest | Monitoring des métriques | Supervision des services |
| **Grafana** | Latest | Visualisation des métriques | Tableaux de bord et alertes |
| **ELK Stack (Elasticsearch, Logstash, Kibana)** | Latest | Centralisation et analyse des logs | Gestion des logs backend et frontend |

---

### **6️⃣ Sécurité**  

| Technologie | Version | Raison du choix | Usage |
|-------------|---------|-----------------|-------|
| **OAuth2 / JWT / Keyclock** | Latest | Authentification sécurisée | API et utilisateurs |
| **Vault** | Latest | Gestion des secrets | Stockage des clés et credentials |
| **Fail2Ban** | Latest | Protection contre les attaques | Sécurisation des serveurs |

## **Workflow de Développement**

### **Branches de Développement**

- **`develop` (Environnement de développement)** :
  - Protégée contre les pushs directs.
  - Merge accepté uniquement avec des branches de `feature/`, `bugfix/`, ou `hotfix/`.
  - Pull requests non obligatoires pour accélérer le développement.
  - Pipeline CI/CD adaptée pour le développement (à intégrer).

- **`test` (Environnement de test)** :
  - Protégée contre les pushs directs.
  - Merge impossible sans pull request depuis `develop`.
  - Pull requests obligatoires pour garantir la qualité avant la mise en environnemnt de test.
  - Pipeline CI/CD adaptée pour l'intégration des tests (à intégrer).

- **`release/MSPR-{tag}` (Préparation de la version)** :
  - Protégée contre les pushs directs.
  - Merge impossible sans pull request depuis `test`.
  - Pull requests obligatoires pour garantir la qualité avant la mise en production.
  - Pipeline CI adaptée pour l'intégration (à intégrer).

- **`main` (Environnement de production)** :
  - Protégée contre les pushs directs.
  - Merge impossible sans pull request depuis `release` ou `hotfix`.
  - Pull requests obligatoires pour assurer la stabilité et la qualité.
  - Pipeline CI/CD adaptée pour la production (à intégrer).

- **`feature/MSPR-{code_projet}_nom_de_la_branche` (Nouvelle fonctionnalité)** :
  - Aucune protection spécifique.
  - Pipeline CI adaptée pour la branche (à intégrer).
  - Merge possible en `develop` après validation.

- **`bugfix/MSPR-{code_projet}_nom_de_la_branche` (Correction de bug)** :
  - Aucune protection spécifique.
  - Pipeline CI adaptée pour la branche (à intégrer).
  - Merge possible en `develop` après validation.

- **`hotfix/MSPR-{code_projet}_nom_de_la_branche` (Correction critique)** :
  - Aucune protection spécifique.
  - Pipeline CI adaptée pour la branche (à intégrer).
  - Merge possible en `develop` et `main` après validation.
  - Pull request obligatoire pour `main`.

### **Schéma :**

```mermaid
%%{init: { 'logLevel': 'debug', 'theme': 'base' } }%%

---
title: Workflow de Développement (GitFlow)
---
gitGraph
  commit
  branch release/MSPR-1.0
  branch test
  branch hotfix/MSPR-001_nom_de_la_branche
  checkout hotfix/MSPR-001_nom_de_la_branche
  branch develop
  checkout develop
  commit id:"ash" tag:"abc"
  branch feature/MSPR-1_nom_de_la_branche
  checkout feature/MSPR-1_nom_de_la_branche
  commit type:HIGHLIGHT
  checkout main
  checkout hotfix/MSPR-001_nom_de_la_branche
  commit type:NORMAL
  checkout develop
  commit type:REVERSE
  checkout feature/MSPR-1_nom_de_la_branche
  commit
  checkout main
  merge hotfix/MSPR-001_nom_de_la_branche
  checkout feature/MSPR-1_nom_de_la_branche
  commit
  checkout develop
  branch bugfix/MSPR-2_nom_de_la_branche
  commit
  checkout develop
  merge hotfix/MSPR-001_nom_de_la_branche
  checkout bugfix/MSPR-2_nom_de_la_branche
  commit
  checkout feature/MSPR-1_nom_de_la_branche
  commit
  checkout develop
  merge bugfix/MSPR-2_nom_de_la_branche
  commit type:REVERSE
  checkout test
  merge develop
  checkout feature/MSPR-1_nom_de_la_branche
  commit
  commit
  checkout develop
  merge feature/MSPR-1_nom_de_la_branche
  checkout release/MSPR-1.0
  merge test
  checkout main
  commit
  checkout main
  merge release/MSPR-1.0
  checkout develop
  merge release/MSPR-1.0
```

## Installation

### 1. **Clonage du projet**  

Pour cloner le dépôt principal pour la première fois, exécutez :

```bash
git clone https://github.com/Sam-rst/EPSI_B3_MSPR-Groupe_MATS.git
cd EPSI_B3_MSPR-Groupe_MATS
```

### 2. **Initialisation de l'environnement**

Bien penser à créer un fichier `.env` à la racine du projet avec les variables d'environnement nécessaires.

```bash
cp config/env/dev.conf .env
```

Note : Insérer vos credentials dans le fichier `.env`.

Pour initialiser l'environnement de développement, exécutez :

```bash
docker-compose up --build -d
```

Pour regarder les logs d'un container, exécutez :

```bash
docker logs -f MSPR-ETL
```

Pour rentrer dans un container, exécutez :

```bash
docker exec -it <container> /bin/bash
```

Pour effectuer tous les tests dans le container :

```bash
python -m unittest discover -f tests -v
```

### 3. **Accès aux services**

- **API REST** : [http://localhost:8000/docs](http://localhost:8000/docs)
- **API ETL** : [http://localhost:8080/docs](http://localhost:8080/docs)

---
