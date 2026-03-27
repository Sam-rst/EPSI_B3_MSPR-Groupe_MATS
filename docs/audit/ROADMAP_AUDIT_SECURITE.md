# Roadmap - Audit Securite Approfondi AnalyzeIT

## 1. Contexte du projet

| Element | Detail |
|---------|--------|
| **Nom** | AnalyzeIT - Groupe MATS |
| **Objectif** | Plateforme d'analyse de donnees epidemiologiques (ETL + API + Frontend + ML) |
| **Utilisateurs** | Analystes sante, administrateurs, data scientists |
| **Donnees manipulees** | Donnees epidemiologiques (continents, pays, epidemies, vaccins, statistiques quotidiennes) |
| **Donnees sensibles** | Identifiants utilisateurs (email, mot de passe), tokens JWT, credentials admin, donnees de sante |
| **Stack** | FastAPI (Python) / Next.js 15 / PostgreSQL / Docker Compose / CircleCI |

---

## 2. Perimetre d'analyse

| Composant | Perimetre |
|-----------|-----------|
| **API REST** | Endpoints CRUD, authentification JWT, rate limiting, validation des entrees |
| **Authentification** | Register, login, verification token, gestion des sessions JWT |
| **Base de donnees** | Schema PostgreSQL, requetes SQL, gestion des credentials |
| **Frontend** | Next.js, appels API, gestion du token cote client |
| **Configuration** | Variables d'environnement, secrets, fichiers .env commites |
| **Dependencies** | Packages Python (requirements.txt) et Node.js (package.json) |
| **Infrastructure** | Docker Compose, Dockerfiles, CI/CD CircleCI |
| **Services tiers** | Metabase, SonarQube |

---

## 3. Cartographie des flux

```
┌─────────────┐     HTTPS      ┌──────────────┐     SQL       ┌──────────────┐
│  Frontend   │ ──────────────>│   API REST   │ ────────────>│  PostgreSQL  │
│  Next.js    │   JWT Bearer   │   FastAPI    │              │              │
│  :3030      │ <──────────────│   :8000      │ <────────────│   :5432      │
└─────────────┘                └──────────────┘              └──────────────┘
                                     │                              │
                                     │ JWT                          │
                                     v                              v
                               ┌──────────────┐            ┌──────────────┐
                               │   Seeder     │            │   Metabase   │
                               │   (init)     │            │   :3000      │
                               └──────────────┘            └──────────────┘

┌─────────────┐   psycopg2     ┌──────────────┐
│  ETL App    │ ──────────────>│  PostgreSQL  │
│  (Tkinter)  │   + API calls  │              │
└─────────────┘                └──────────────┘
```

---

## 4. Plan d'audit - 6 constats minimum

### Constats lies au Chapitre 4 - Seance 4 : Attaques web et mecanismes navigateur (XSS, SQLi, CSRF, IDOR, SSTI, SOP, CORS, CSP)

| # | Constat a investiguer | OWASP | Fichiers cles | Lien cours |
|---|----------------------|-------|---------------|------------|
| C1 | **Injection SQL / Validation des entrees** - Verifier la sanitization des inputs sur les endpoints CRUD et import en masse | A03 Injection | `apps/api/src/app/*/infrastructure/`, routers | Seance 4 - SQLi |
| C2 | **Headers de securite HTTP manquants** - Verifier CORS (trop permissif ?), CSP absent, X-Frame-Options, HSTS | A05 Mauvaise config | `apps/api/src/main.py`, config Next.js | Seance 4 - CORS/CSP |
| C3 | **IDOR / Controle d'acces defaillant** - Verifier si un user authentifie peut acceder aux donnees d'un autre via manipulation d'ID | A01 Controle acces | Routers CRUD (continents, countries, users, etc.) | Seance 4 - IDOR |

### Constats lies au Chapitre 5 - Seance 5 : Principes de securisation (privileges, mots de passe, cookies, HTTPS/TLS, services tiers)

| # | Constat a investiguer | OWASP | Fichiers cles | Lien cours |
|---|----------------------|-------|---------------|------------|
| C4 | **Hashage des mots de passe** - Verifier si les mots de passe sont hashes (bcrypt/argon2) ou stockes en clair en BDD | A02 Defaillances crypto | `apps/api/src/app/auth/`, `apps/api/src/app/user/` | Seance 5 - Gestion MDP |
| C5 | **Secrets commites dans le repo Git** - JWT_SECRET_KEY, ADMIN_PASSWORD, SONAR_TOKEN en clair dans l'historique | A05 Mauvaise config | `.env`, `config/env/*.conf`, historique Git | Seance 5 - Services tiers / cles API |
| C6 | **Gestion JWT incomplete** - Pas de refresh token, pas de revocation, forgot-password non implemente, pas de cookie securise | A07 Defauts auth | `apps/api/src/core/auth/authorizer.py`, `dependencies.py` | Seance 5 - Cookies / sessions |

### Constats supplementaires (Supply chain - pour section DependencyCheck + SonarQube)

| # | Constat a investiguer | OWASP | Fichiers cles | Lien cours |
|---|----------------------|-------|---------------|------------|
| C7 | **Dependencies vulnerables** - Analyser les CVE connues sur les packages Python et Node.js | A06 Composants vulnerables | `apps/api/requirements.txt`, `apps/frontend/package.json` | Seance 3 - SCA |
| C8 | **Images Docker non pinees** - `postgres:latest`, `metabase/metabase:latest` sans hash digest | A08 Defauts integrite | `docker-compose.yml`, `Dockerfile` | Seance 5 - Services tiers |

---

## 5. Roadmap des taches

### Phase 1 : Analyse statique du code (Chapitre 4)

- [ ] **1.1** Scanner les secrets dans l'historique Git avec `gitleaks` ou `trufflehog`
  - Cible : `.env`, `config/env/`, commits passes
  - Preuve : liste des secrets trouves + commits concernes

- [ ] **1.2** Auditer le mecanisme d'authentification
  - Verifier le hashage des mots de passe (bcrypt ? argon2 ? clair ?)
  - Verifier la creation/validation JWT (algorithme, expiration, claims)
  - Verifier l'absence de refresh token et de revocation
  - Cible : `apps/api/src/app/auth/`, `apps/api/src/core/auth/`

- [ ] **1.3** Auditer la validation des entrees
  - Verifier les schemas Pydantic sur chaque endpoint
  - Tester les injections SQL via SQLAlchemy (ORM vs raw queries)
  - Verifier les endpoints d'import en masse (bulk import)
  - Cible : tous les routers et usecases dans `apps/api/src/app/`

- [ ] **1.4** Verifier les headers de securite HTTP
  - CORS : origines autorisees ?
  - CSP, X-Content-Type-Options, X-Frame-Options, Strict-Transport-Security
  - Cible : `apps/api/src/main.py`, configuration Next.js

### Phase 2 : Analyse supply chain (Chapitre 5)

- [ ] **2.1** Lancer OWASP Dependency-Check
  - Analyser `apps/api/requirements.txt`
  - Analyser `apps/frontend/package.json` + `package-lock.json`
  - Selectionner les 3 CVE les plus critiques

- [ ] **2.2** Analyser les images Docker
  - Verifier les versions pinees vs `latest`
  - Scanner avec `trivy` les images utilisees
  - Identifier les vulnerabilites dans les images de base

- [ ] **2.3** Configurer et lancer SonarQube Cloud
  - Importer le depot sur SonarQube Cloud
  - Lancer l'analyse sur `main`
  - Relever Quality Gate, issues, Security Hotspots
  - Selectionner 5 elements max pertinents pour l'audit

- [ ] **2.4** (Bonus) Installer SonarLint dans l'IDE
  - Comparer les resultats IDE vs Cloud
  - Expliquer les differences

### Phase 3 : Tests dynamiques

- [ ] **3.1** Tester les endpoints API avec curl/Postman
  - Tenter des requetes sans token
  - Tenter des requetes avec token expire/invalide
  - Tester le rate limiting (depasser les limites)
  - Tester les injections via les champs de saisie

- [ ] **3.2** Verifier les cookies et sessions
  - Flags HttpOnly, Secure, SameSite
  - Comportement du token JWT cote client

### Phase 4 : Synthese et livrables

- [ ] **4.1** Rediger les 6+ fiches de constat
  - Pour chaque constat : preuve, scenario d'exploitation, impact, vraisemblance, priorite
  - Corrections : immediate, durable, methode de verification

- [ ] **4.2** Construire la matrice de priorisation des risques
  - Axes : vraisemblance x impact
  - Classifier chaque constat

- [ ] **4.3** Definir le top 3 des risques prioritaires

- [ ] **4.4** Rediger le plan d'actions
  - Court terme (corrections immediates)
  - Moyen terme (corrections durables)
  - Structurel (mesures de fond)

- [ ] **4.5** Preparer le support de soutenance (10min max)
  - Contexte + perimetre
  - 6 constats
  - Top 3 risques
  - 1 minute Supply Chain (SonarQube + Dependency-Check)
  - Plan de securisation

- [ ] **4.6** Documenter l'usage de l'IA
  - Ce que l'IA a propose
  - Ce qui a ete garde / rejete / verifie

---

## 6. Premiers constats deja identifies (pre-audit)

> Ces constats sont issus de la lecture initiale du code et doivent etre confirmes par des preuves.

### CRITIQUE - Secrets commites dans Git
- **Preuve** : Le fichier `.env` est dans `.gitignore` MAIS les valeurs sont visibles dans les fichiers `config/env/*.conf` commites, et surtout le `.env` a potentiellement ete commite dans l'historique
- **Donnees exposees** : `JWT_SECRET_KEY`, `ADMIN_PASSWORD`, `SONAR_TOKEN`, `MB_DB_PASS`
- **Impact** : Compromission totale de l'authentification si la cle JWT est connue

### ELEVE - Mot de passe admin faible et en dur
- **Preuve** : `ADMIN_USERNAME=admin.admin`, `ADMIN_PASSWORD=Admin54321!` dans `.env`
- **Impact** : Acces administrateur par defaut si non change en production

### MOYEN - Images Docker non pinees
- **Preuve** : `postgres:latest`, `metabase/metabase:latest` dans `docker-compose.yml`
- **Impact** : Regression de securite silencieuse, supply chain attack possible

### A VERIFIER - Hashage des mots de passe
- **A confirmer** : Lecture du code d'enregistrement dans `apps/api/src/app/auth/`

---

## 7. Outils a utiliser

| Outil | Usage | Priorite |
|-------|-------|----------|
| **Gitleaks** | Recherche de secrets dans l'historique Git | Obligatoire |
| **OWASP Dependency-Check** | Analyse CVE des dependencies | Obligatoire |
| **SonarQube Cloud** | Analyse qualite et securite du code | Obligatoire |
| **SonarLint (IDE)** | Analyse locale temps reel | Bonus |
| **curl / Postman** | Tests API dynamiques | Obligatoire |
| **Trivy** | Scan des images Docker | Recommande |
| **DevTools navigateur** | Verification headers HTTP | Obligatoire |

---

## 8. Planning estime

| Phase | Description | Duree |
|-------|-------------|-------|
| Phase 1 | Analyse statique du code | ~2h |
| Phase 2 | Analyse supply chain | ~2h |
| Phase 3 | Tests dynamiques | ~1h |
| Phase 4 | Synthese et livrables | ~2h |
| **Total** | | **~7h** |
