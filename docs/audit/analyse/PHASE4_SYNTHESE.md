# Phase 4 - Synthese de l'audit securite

## 4.1 Fiches de constat

---

### CONSTAT C4 - Hashage des mots de passe SHA256 sans salt

| Champ | Detail |
|-------|--------|
| **Chapitre** | 5 - Principes de securisation (Gestion des mots de passe) |
| **OWASP** | A02 - Defaillances cryptographiques |
| **Severite** | CRITIQUE |

**Preuve :**
- `apps/api/src/app/user/infrastructure/repository/user_repo_in_postgres.py` ligne 33 : `hashlib.sha256(payload.password.encode()).hexdigest()`
- Aucune dependance bcrypt/argon2 dans `requirements.txt`
- Test dynamique : `GET /users/id/1` retourne le hash en clair `"password":"64eb837..."`
- Test BDD directe : `SELECT password FROM "user"` confirme SHA256 64 chars hex sans salt

**Scenario d'exploitation :**
1. Attaquant authentifie appelle `GET /users/id/{id}` pour recuperer le hash SHA256
2. Ou bien accede directement a la BDD via port 5432 expose
3. Utilise hashcat/john avec GPU pour casser le SHA256 sans salt en secondes
4. Mots de passe identiques = memes hash (pas de salt) -> attaque par rainbow table

**Impact :** Compromission de tous les comptes utilisateurs. Avec SHA256 sans salt, un GPU moderne peut tester ~10 milliards de hash/seconde.

**Vraisemblance :** Elevee - Le hash est accessible via l'API et la BDD est exposee

**Priorite :** P1

**Correction immediate :** Remplacer par `bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))`

**Correction durable :** Ajouter `bcrypt` aux dependances. Migrer les hash existants (re-hash au login). Supprimer le champ `password` des reponses API (ne jamais exposer le hash)

**Verification :** Les hash en BDD doivent commencer par `$2b$12$` (bcrypt). `GET /users/id/{id}` ne doit plus contenir le champ `password`

---

### CONSTAT C3 - Controle d'acces defaillant (IDOR)

| Champ | Detail |
|-------|--------|
| **Chapitre** | 4 - Attaques web (IDOR) |
| **OWASP** | A01 - Controle d'acces defaillant |
| **Severite** | CRITIQUE |

**Preuve :**
- Test dynamique : `DELETE /users/1` avec le token de user2 -> `200 "L'utilisateur 'Audit Test' a bien ete supprime."`
- `GET /users/id/1` avec n'importe quel token retourne les donnees completes (y compris le hash du mot de passe)
- 20+ endpoints CRUD affectes (continents, countries, epidemics, vaccines, users, roles)
- Les usecases ne recoivent que l'`id`, jamais le contexte utilisateur
- L'entite `Role` existe en BDD mais aucun RBAC n'est implemente

**Scenario d'exploitation :**
1. Attaquant cree un compte (register)
2. Itere sur `GET /users/id/1`, `GET /users/id/2`, etc. pour enumerer tous les utilisateurs
3. Recupere les hash de mots de passe de tous les comptes
4. Peut supprimer/modifier n'importe quelle donnee via PUT/DELETE

**Impact :** Acces, modification et suppression non autorises de toutes les donnees du systeme

**Vraisemblance :** Elevee - Trivial a exploiter (simple modification d'ID dans l'URL)

**Priorite :** P1

**Correction immediate :** Ajouter une verification `current_user.id == resource.owner_id` ou `current_user.role == "admin"` sur chaque endpoint d'ecriture

**Correction durable :** Implementer un middleware RBAC. Definir des permissions par role (admin, analyste, lecteur). Injecter le `current_user` dans tous les usecases

**Verification :** Un utilisateur non-admin qui appelle `DELETE /users/{autre_id}` doit recevoir un `403 Forbidden`

---

### CONSTAT C2 - Absence de headers de securite HTTP et CORS

| Champ | Detail |
|-------|--------|
| **Chapitre** | 4 - Attaques web (CORS, CSP, SOP) |
| **OWASP** | A05 - Mauvaise configuration de securite |
| **Severite** | ELEVEE |

**Preuve :**
- Test dynamique `curl -D -` sur l'API et le frontend : aucun header de securite
- `apps/api/src/main.py` : pas de CORSMiddleware configure (variables definies dans `config.py` mais jamais utilisees)
- Swagger `/docs` accessible sans authentification (expose toute la structure API)
- Frontend expose `X-Powered-By: Next.js` (fingerprinting)
- 49+ fichiers leakent les stack traces dans les reponses d'erreur (`detail=f"...{str(e)}"`)
- Test dynamique : erreur 500 renvoie la requete SQL complete, les noms de tables et colonnes

**Scenario d'exploitation :**
1. Attaquant consulte `/docs` pour cartographier tous les endpoints
2. Provoque des erreurs pour obtenir les noms de tables/colonnes via les stack traces
3. Utilise ces informations pour cibler les attaques IDOR et d'enumeration
4. Sans CSP, une XSS permettrait de voler les tokens JWT stockes en localStorage

**Impact :** Facilite la reconnaissance, elargit la surface d'attaque, expose des informations internes

**Vraisemblance :** Elevee - `/docs` est public, les stack traces sont systematiques

**Priorite :** P1

**Correction immediate :** Ajouter un middleware FastAPI avec les headers essentiels. Desactiver `/docs` en production (`docs_url=None if ENV=="prod"`)

**Correction durable :** Configurer CORS avec whitelist stricte. Ajouter CSP, HSTS, X-Frame-Options. Implementer un handler d'erreur global qui log l'erreur mais renvoie un message generique. Supprimer `X-Powered-By` du frontend

**Verification :** `curl -I http://api/` doit retourner les headers CSP, HSTS, X-Frame-Options. `/docs` doit renvoyer 404 en production

---

### CONSTAT C6 - Gestion JWT incomplete et enumeration d'utilisateurs

| Champ | Detail |
|-------|--------|
| **Chapitre** | 5 - Principes de securisation (Cookies, sessions, authentification) |
| **OWASP** | A07 - Defauts d'identification et d'authentification |
| **Severite** | ELEVEE |

**Preuve :**
- Test dynamique login : 3 messages d'erreur differents (`"format firstname.lastname"`, `"username n'existe pas"`, `"Mot de passe incorrect"`) permettent l'enumeration
- Pas de refresh token : `JWT_REFRESH_TOKEN_EXPIRES` defini dans settings.py mais jamais implemente
- Pas de blacklist : `JWT_BLACKLIST_ENABLED` defini mais jamais implemente
- Token retourne dans le body JSON (pas de cookie HttpOnly/Secure/SameSite)
- JWT contient des donnees personnelles en clair (email, nom, prenom) lisibles par decode base64
- Pas de lockout apres echecs de connexion
- Comparaison de hash non constante (`==` au lieu de `hmac.compare_digest()`)

**Scenario d'exploitation :**
1. Attaquant teste des usernames au format `prenom.nom` pour enumerer les comptes
2. Brute-force le mot de passe (rate limit 5/min mais pas de lockout)
3. Token obtenu stocke en localStorage (volable par XSS)
4. Token non revocable pendant 1h meme apres changement de mot de passe

**Impact :** Compromission de comptes, impossibilite de revoquer un token vole

**Vraisemblance :** Moyenne a elevee

**Priorite :** P1

**Correction immediate :** Uniformiser le message d'erreur : `"Identifiants invalides."`. Supprimer les donnees personnelles du JWT (garder `sub`, `id`, `role_id`, `exp`)

**Correction durable :** Implementer refresh tokens, blacklist Redis, lockout apres 5 echecs. Stocker le token dans un cookie HttpOnly/Secure/SameSite=Strict

**Verification :** Tester que la reponse login est identique quel que soit le cas d'erreur. Verifier que le JWT ne contient plus d'email/nom

---

### CONSTAT C5 - Secrets en clair et credentials par defaut

| Champ | Detail |
|-------|--------|
| **Chapitre** | 5 - Principes de securisation (Services tiers, cles API) |
| **OWASP** | A05 - Mauvaise configuration de securite |
| **Severite** | ELEVEE |

**Preuve :**
- `.env` local contient `JWT_SECRET_KEY`, `ADMIN_PASSWORD=Admin54321!`, `SONAR_TOKEN`, `MB_DB_PASS` en clair
- `.env` dans `.gitignore` (bon point) mais jamais commite par erreur non plus
- SonarQube Cloud a detecte 3 issues S2068 : credentials hardcodees en fallback dans le code :
  - `apps/etl/src/app/auth/db_connector.py` L23 : `os.environ.get("ETL_POSTGRES_PASSWORD", "postgres")`
  - `apps/.../load.py` L16 : `password="postgres"` en defaut du constructeur
  - `apps/seeder/src/main.py` L8 : `os.getenv("ADMIN_PASSWORD", "admin")` fallback
- Mot de passe admin par defaut `Admin54321!` faible et previsible
- Test dynamique : BDD accessible directement avec `postgres/postgres`

**Scenario d'exploitation :**
Si les variables d'environnement ne sont pas definies, le systeme utilise les fallbacks hardcodes. Un attaquant qui connait le code source (repo public) connait les credentials par defaut.

**Impact :** Acces complet au systeme avec les credentials par defaut

**Vraisemblance :** Elevee (repo GitHub public, credentials par defaut triviaux)

**Priorite :** P1

**Correction immediate :** Supprimer tous les fallbacks par defaut. Generer des mots de passe forts aleatoires. Faire echouer l'application si les variables d'environnement ne sont pas definies

**Correction durable :** Utiliser un gestionnaire de secrets (Vault, Docker Secrets). Implementer la rotation automatique. Rendre le repo prive ou nettoyer l'historique

**Verification :** L'application ne doit pas demarrer si `JWT_SECRET_KEY` ou `ADMIN_PASSWORD` ne sont pas definis

---

### CONSTAT C7 - Dependencies non pinees (Supply chain)

| Champ | Detail |
|-------|--------|
| **Chapitre** | Supply chain (Seance 3 - SCA) |
| **OWASP** | A06 - Composants vulnerables et obsoletes |
| **Severite** | ELEVEE |

**Preuve :**
- `apps/api/requirements.txt` : 10/10 dependances sans aucune version (`fastapi`, `uvicorn`, `sqlalchemy`...)
- Pas de lock file Python (pas de `poetry.lock` ni `pip freeze`)
- `postgres:latest` cause un crash au deploy (v18 incompatible, constate en Phase 3)
- Images Docker non pinees : `python:3.10`, `node:20-alpine`, `metabase/metabase:latest`
- CI/CD CircleCI : images `cimg/python:3.11` non pinees

**Scenario d'exploitation :**
1. Un package PyPI est compromis (typosquatting, account takeover)
2. Le prochain `pip install` installe la version malveillante sans verification
3. Le meme package est deploye en production via la CI/CD
4. Demonstration concrete : `postgres:latest` = v18 a casse le systeme au deploy

**Impact :** Execution de code arbitraire en production, instabilite du systeme

**Vraisemblance :** Moyenne (attaques supply chain en hausse) - **CONFIRMEE** par le crash postgres:latest

**Priorite :** P1

**Correction immediate :** `pip freeze > requirements.txt` pour piner toutes les versions. Piner les images Docker (`postgres:17.4`, `python:3.10.14-slim`)

**Correction durable :** Adopter Poetry avec lock file. Ajouter `pip-audit` et Trivy dans la CI/CD. Generer un SBOM

**Verification :** Chaque ligne de requirements.txt contient `==x.y.z`. Chaque image Docker a un tag de version specifique

---

### CONSTAT C8 - Infrastructure Docker non securisee

| Champ | Detail |
|-------|--------|
| **Chapitre** | Supply chain (Seance 5 - Services tiers) |
| **OWASP** | A08 - Defauts d'integrite des logiciels et donnees |
| **Severite** | ELEVEE |

**Preuve :**
- Port PostgreSQL expose en externe (`${POSTGRES_PORT}:5432` dans docker-compose.yml)
- Test dynamique : acces direct a la BDD avec `psql -U postgres -d mspr` -> listing de tous les users et hash
- Tous les containers executent en root (pas de directive `USER` dans les Dockerfiles)
- SonarQube : 5 hotspots confirment (docker:S6470, docker:S6471)
- Pas de `.dockerignore` (risque de copier des secrets dans l'image)
- Pas de health check sur db, api, frontend
- SSH deploy CI/CD sans `StrictHostKeyChecking` (MITM)
- Volume Metabase monte sur `/dev/random:ro` (misconfiguration)

**Scenario d'exploitation :**
1. Attaquant scanne le port 5432 ouvert
2. Se connecte avec `postgres/postgres`
3. Extrait toutes les donnees (users, hash, donnees epidemiologiques)
4. Ou bien : container escape sur un container root = controle total du host

**Impact :** Acces direct a la BDD, elevation de privileges via container root

**Vraisemblance :** Elevee (port expose, credentials par defaut)

**Priorite :** P1

**Correction immediate :** Supprimer le port expose PostgreSQL. Ajouter `USER appuser` dans les Dockerfiles

**Correction durable :** Creer `.dockerignore`. Ajouter health checks. Fixer `StrictHostKeyChecking=accept-new` en CI. Ajouter resource limits. Fixer le volume Metabase

**Verification :** `docker exec <container> whoami` doit retourner un user non-root. `nmap localhost -p 5432` ne doit pas trouver le port ouvert

---

## 4.2 Matrice de priorisation des risques

```
                        IMPACT
                 Faible    Moyen     Eleve    Critique
              ┌──────────┬─────────┬─────────┬──────────┐
   Elevee     │          │         │ C5, C6  │ C4, C3   │
              │          │         │ C7      │ C2, C8   │
              ├──────────┼─────────┼─────────┼──────────┤
V  Moyenne    │          │         │ C1      │          │
R             │          │         │         │          │
A  ├──────────┼─────────┼─────────┼──────────┤
I  Faible     │          │         │         │          │
S             │          │         │         │          │
S  └──────────┴─────────┴─────────┴──────────┘
E
M
B
L
A
N
C
E
```

| Constat | Vraisemblance | Impact | Zone |
|---------|---------------|--------|------|
| **C4** - SHA256 sans salt | Elevee | Critique | **CRITIQUE** |
| **C3** - IDOR / pas de RBAC | Elevee | Critique | **CRITIQUE** |
| **C2** - Pas de headers / stack traces | Elevee | Critique | **CRITIQUE** |
| **C8** - Docker non securise / BDD exposee | Elevee | Critique | **CRITIQUE** |
| **C5** - Secrets / credentials par defaut | Elevee | Eleve | **ELEVE** |
| **C6** - JWT incomplet / enumeration | Elevee | Eleve | **ELEVE** |
| **C7** - Dependencies non pinees | Elevee | Eleve | **ELEVE** |
| **C1** - Validation Pydantic insuffisante | Moyenne | Eleve | **MOYEN** |

---

## 4.3 Top 3 des risques prioritaires

### Risque 1 : Compromission des comptes via SHA256 + IDOR (C4 + C3)

**Justification :** La combinaison de SHA256 sans salt ET de l'exposition du hash via l'API (`GET /users/id/{id}` retourne le champ `password`) permet a n'importe quel utilisateur authentifie de recuperer et casser les mots de passe de tous les autres utilisateurs en quelques secondes. C'est la faille la plus critique car elle permet une compromission totale sans competence technique avancee.

**Actions :** Remplacer SHA256 par bcrypt, supprimer le hash des reponses API, implementer RBAC

---

### Risque 2 : Acces direct a la BDD et infrastructure non securisee (C8 + C5)

**Justification :** Le port PostgreSQL 5432 est expose avec les credentials par defaut `postgres/postgres`. Un attaquant peut acceder a l'integralite des donnees sans meme passer par l'API. Les containers root et le SSH sans verification de cle aggravent le risque. La demonstration concrete avec `postgres:latest` (crash v18) prouve que l'infra n'est pas maitrisee.

**Actions :** Fermer le port 5432, supprimer les credentials par defaut, ajouter USER non-root, piner les images

---

### Risque 3 : Absence de defense en profondeur sur l'API (C2 + C6)

**Justification :** L'API n'a aucune couche de protection : pas de CORS, pas de CSP, pas de HSTS, Swagger expose publiquement, stack traces completes renvoyees aux clients, enumeration d'utilisateurs possible, pas de revocation de tokens. Un attaquant dispose de toutes les informations necessaires pour planifier et executer une attaque ciblee.

**Actions :** Ajouter headers securite, desactiver /docs en prod, uniformiser les erreurs, implementer refresh/blacklist JWT

---

## 4.4 Plan d'actions

### Court terme (1-2 jours)

| # | Action | Constats | Effort |
|---|--------|----------|--------|
| 1 | Remplacer `hashlib.sha256` par `bcrypt` (12 rounds) | C4 | 2h |
| 2 | Supprimer le champ `password` des reponses API (UserResponse) | C3, C4 | 30min |
| 3 | Uniformiser le message d'erreur login : `"Identifiants invalides."` | C6 | 30min |
| 4 | Supprimer le port expose PostgreSQL du docker-compose | C8 | 5min |
| 5 | Desactiver `/docs` en production | C2 | 15min |
| 6 | Piner toutes les dependances (`pip freeze`, images Docker) | C7, C8 | 1h |
| 7 | Supprimer les fallbacks de credentials hardcodes | C5 | 30min |

### Moyen terme (1-2 semaines)

| # | Action | Constats | Effort |
|---|--------|----------|--------|
| 8 | Ajouter un middleware headers securite (CORS, CSP, HSTS, X-Frame-Options) | C2 | 2h |
| 9 | Implementer un handler d'erreur global (pas de stack trace en reponse) | C2 | 3h |
| 10 | Implementer RBAC avec verification de role sur tous les endpoints | C3 | 1-2j |
| 11 | Ajouter `USER appuser` dans tous les Dockerfiles + `.dockerignore` | C8 | 2h |
| 12 | Ajouter des validations Pydantic (max_length, pattern, ge=0) | C1 | 3h |
| 13 | Supprimer les donnees personnelles du JWT (garder sub, id, role, exp) | C6 | 1h |
| 14 | Ajouter `pip-audit` et Trivy dans la CI/CD | C7 | 2h |

### Structurel (1-3 mois)

| # | Action | Constats | Effort |
|---|--------|----------|--------|
| 15 | Implementer refresh tokens + blacklist (Redis) | C6 | 3-5j |
| 16 | Mettre en place un gestionnaire de secrets (Vault / Docker Secrets) | C5 | 2-3j |
| 17 | Adopter Poetry avec lock file pour tous les projets Python | C7 | 1j |
| 18 | Ajouter lockout de compte apres 5 echecs de login | C6 | 1j |
| 19 | Stocker le JWT en cookie HttpOnly/Secure/SameSite au lieu de localStorage | C6 | 2j |
| 20 | Mettre en place un reverse proxy (nginx/traefik) avec TLS termination | C2, C8 | 2j |
| 21 | Generer un SBOM et mettre en place la signature d'images Docker | C7, C8 | 2j |
| 22 | Ajouter des tests de securite automatises dans la CI (non vides) | C7 | 2j |

---

## 4.5 Usage de l'IA dans cet audit

### Ce que l'IA (Claude Code) a propose

- Analyse automatisee du code source en parallele (4 agents simultanees pour Phase 1)
- Identification des fichiers cles et des patterns de vulnerabilites
- Mapping des constats sur les references OWASP Top 10
- Generation des commandes curl pour les tests dynamiques
- Redaction structuree des fiches de constat avec le format preuve/scenario/impact/correction
- Resolution du crash `postgres:latest` (tag postgres:17 comme workaround)

### Ce que nous avons garde

- Tous les constats identifies par l'IA ont ete **confirmes par des preuves concretes** (tests dynamiques, SonarQube, lecture du code)
- La structure des rapports et le mapping OWASP
- Les recommandations de correction (bcrypt, RBAC, headers securite)
- L'analyse des resultats SonarQube (distinction faux positif vs vrai risque)

### Ce que nous avons rejete

- Certaines severites initiales ont ete ajustees apres verification manuelle
- L'IA avait suppose que le `.env` etait commite dans Git -> verification a prouve que non (`.gitignore` OK)
- Le constat initial sur l'injection SQL a ete reduit apres verification : l'ORM SQLAlchemy est utilise correctement partout

### Ce que nous avons verifie

- **Chaque constat** a ete valide par au moins une preuve concrete :
  - C4 (SHA256) : hash en BDD + hash dans la reponse API + absence de bcrypt dans requirements
  - C3 (IDOR) : `DELETE /users/1` avec le token d'un autre utilisateur = 200 OK
  - C2 (headers) : `curl -D -` montre zero headers de securite
  - C6 (enumeration) : 3 messages d'erreur differents au login
  - C5 (secrets) : SonarQube S2068 + analyse du code
  - C7 (supply chain) : crash `postgres:latest` v18 au deploy
  - C8 (Docker) : `psql` direct sur port 5432 avec `postgres/postgres`
- Les resultats SonarQube Cloud et SonarLint ont confirme les constats manuels
- Les faux positifs SonarQube (traductions UI) ont ete correctement ecartes
