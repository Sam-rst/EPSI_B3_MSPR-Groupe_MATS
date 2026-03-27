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

### Phase 1 : Analyse statique du code (Chapitre 4 + 5) - TERMINEE

- [x] **1.1** Scanner les secrets dans l'historique Git
  - Resultat : `.env` jamais commite (`.gitignore` OK). Secrets en clair dans `.env` local uniquement
  - Rapport : `docs/audit/PHASE1_ANALYSE_STATIQUE.md` > C5

- [x] **1.2** Auditer le mecanisme d'authentification
  - Resultat : **SHA256 sans salt** au lieu de bcrypt (CRITIQUE). Enumeration d'utilisateurs, pas de refresh token/blacklist/lockout
  - Rapport : `docs/audit/PHASE1_ANALYSE_STATIQUE.md` > C4, C6

- [x] **1.3** Auditer la validation des entrees
  - Resultat : Pydantic sans contraintes (pas de max_length/pattern). ORM SQLAlchemy OK (pas de SQLi). IDOR sur tous les endpoints CRUD
  - Rapport : `docs/audit/PHASE1_ANALYSE_STATIQUE.md` > C1, C3

- [x] **1.4** Verifier les headers de securite HTTP
  - Resultat : **Zero headers de securite**. CORS non configure. `/docs` expose. 49+ fichiers leakent les stack traces
  - Rapport : `docs/audit/PHASE1_ANALYSE_STATIQUE.md` > C2

### Phase 2 : Analyse supply chain (Chapitre 5) - TERMINEE

- [x] **2.1** Analyser les dependances (OWASP Dependency-Check)
  - Resultat : API = 10/10 deps non pinees, pas de lock file Python. Frontend = OK (package-lock.json)
  - Rapport : `docs/audit/PHASE2_SUPPLY_CHAIN.md` > C7

- [x] **2.2** Analyser les images Docker
  - Resultat : 5 images non pinees, port BDD expose, containers root, pas de .dockerignore
  - Rapport : `docs/audit/PHASE2_SUPPLY_CHAIN.md` > C8

- [x] **2.3** Analyser la pipeline CI/CD
  - Resultat : SSH sans StrictHostKeyChecking, images CI non pinees, tests securite ignores
  - Rapport : `docs/audit/PHASE2_SUPPLY_CHAIN.md`

- [ ] **2.4** SonarQube Cloud (a faire manuellement)
  - Importer le depot, lancer l'analyse sur `main`, relever Quality Gate et Security Hotspots

- [x] **2.5** (Bonus) SonarLint dans l'IDE
  - Resultat : Memes regles securite detectees (S2068, S6470, S6471, S5332). Issues supplementaires de maintenabilite (S108, S112, S1066)
  - Rapport : `docs/audit/PHASE2_SUPPLY_CHAIN.md` > 2.5

### Phase 3 : Tests dynamiques - TERMINEE

- [x] **3.1** Tester les endpoints API avec curl
  - Resultat : 401 OK sans token. Stack traces SQL fuites (CRITIQUE). IDOR confirme (suppression cross-user). Hash mdp retourne dans les reponses API. Enumeration d'utilisateurs confirmee. Rate limiting fonctionnel (429)
  - Rapport : `docs/audit/PHASE3_TESTS_DYNAMIQUES.md`

- [x] **3.2** Verifier cookies et sessions
  - Resultat : Aucun cookie (token en body JSON). Zero headers securite (CSP, HSTS, X-Frame-Options absents). JWT contient donnees personnelles en clair. BDD accessible directement sur port 5432
  - Rapport : `docs/audit/PHASE3_TESTS_DYNAMIQUES.md`

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

## 6. Synthese des constats confirmes

| # | Constat | Chapitre | Severite | OWASP | Phase |
|---|---------|----------|----------|-------|-------|
| C4 | SHA256 sans salt au lieu de bcrypt | Chap 5 | CRITIQUE | A02 | Phase 1 |
| C3 | IDOR - aucun controle d'acces sur 20+ endpoints | Chap 4 | ELEVEE | A01 | Phase 1 |
| C2 | Zero headers securite, CORS absent, `/docs` expose | Chap 4 | ELEVEE | A05 | Phase 1 |
| C6 | JWT sans refresh/blacklist, enumeration de comptes | Chap 5 | ELEVEE | A07 | Phase 1 |
| C5 | Secrets en clair, mdp admin faible, pas de rotation | Chap 5 | ELEVEE | A05 | Phase 1 |
| C1 | Validation Pydantic insuffisante (pas de contraintes) | Chap 4 | MOYENNE | A03 | Phase 1 |
| C7 | 100% deps API non pinees, pas de lock file Python | Supply chain | ELEVEE | A06 | Phase 2 |
| C8 | Images Docker latest, port BDD expose, containers root | Supply chain | ELEVEE | A08 | Phase 2 |

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
