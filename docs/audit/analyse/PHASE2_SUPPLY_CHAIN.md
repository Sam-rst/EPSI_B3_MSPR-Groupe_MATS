# Phase 2 - Analyse Supply Chain

## 2.1 Dependances vulnerables (OWASP Dependency-Check)

### Constat C7 : Dependencies non pinees et sans verification d'integrite (A06)

**Severite : ELEVEE**

**Preuve :**

| Composant | Total deps | Pinees (==) | Non pinees | Lock file | Risque |
|-----------|-----------|-------------|------------|-----------|--------|
| **API** (`apps/api/requirements.txt`) | 10 | **0 (0%)** | 10 (100%) | NON | **CRITIQUE** |
| **Frontend** (`apps/frontend/package.json`) | 10 | 2 | 8 (^) | OUI (`package-lock.json`) | MOYEN |
| **ETL** (`apps/etl/requirements.txt`) | 10 | 8 (80%) | 2 | NON | MOYEN |
| **Seeder** (`apps/seeder/requirements.txt`) | 2 | 0 (0%) | 2 (100%) | NON | MOYEN |

**Detail API (`apps/api/requirements.txt`) - AUCUNE version pince :**
```
fastapi          # non pine
uvicorn          # non pine
sqlalchemy       # non pine
dependency_injector  # non pine
PyJWT            # non pine
python-dotenv    # non pine
psycopg2-binary  # non pine
alembic          # non pine
pylint           # non pine
slowapi          # non pine
```

**Detail ETL - Majoritairement pine :**
```
pandas==2.2.3          # pine
psycopg2-binary==2.9.10  # pine
python-dotenv==1.0.1   # pine
httpx==0.27.0          # pine
requests               # NON pine
pylint                 # NON pine
```

**Scenario d'exploitation :**
Un attaquant compromet un package PyPI (typosquatting ou account takeover). Sans version pinee ni lock file, le prochain `pip install` installe la version malveillante. C'est exactement le scenario de l'attaque SolarWinds / event-stream applique a Python.

**Impact :** Execution de code arbitraire sur le serveur de build et en production

**Vraisemblance :** Moyenne (attaques supply chain en hausse, cf. OWASP A06, A08)

**Priorite :** P1

**Correction immediate :** Piner toutes les dependances API avec `pip freeze > requirements.txt`

**Correction durable :** Adopter `poetry` avec `poetry.lock` pour tous les projets Python. Ajouter `pip-audit` ou OWASP Dependency-Check dans la CI/CD

**Verification :** Verifier que chaque ligne de `requirements.txt` contient `==x.y.z`

---

## 2.2 Images Docker non pinees et configuration dangereuse

### Constat C8 : Images Docker non pinees et mauvaise configuration (A08)

**Severite : ELEVEE**

**Preuve - Images non pinees :**

| Service | Image | Fichier | Probleme |
|---------|-------|---------|----------|
| db | `postgres:latest` | `docker-compose.yml:5` | Tag `latest` |
| metabase | `metabase/metabase:latest` | `docker-compose.yml:48` | Tag `latest` |
| api | `python:3.10` | `apps/api/Dockerfile:1` | Pas de patch version |
| frontend | `node:20-alpine` | `apps/frontend/Dockerfile:2,20` | Pas de patch version |
| seeder | `python:3.11-slim` | `apps/seeder/Dockerfile:2` | Pas de patch version |

**Preuve - Autres problemes Docker :**

| Probleme | Fichier | Ligne | Severite |
|----------|---------|-------|----------|
| **Port BDD expose** (`${POSTGRES_PORT}:5432`) | `docker-compose.yml` | 12-13 | CRITIQUE |
| **Pas de user non-root** (tous les containers) | Tous les Dockerfiles | - | ELEVE |
| **Volume bind mount dev** (`./apps/api:/app`) | `docker-compose.yml` | 27-28 | ELEVE |
| **Pas de health check** sur db, api, frontend | `docker-compose.yml` | - | MOYEN |
| **Pas de .dockerignore** | Tous les apps | - | MOYEN |
| **Volume suspect** metabase -> `/dev/random:ro` | `docker-compose.yml` | 55 | MOYEN |
| **Pas de resource limits** | `docker-compose.yml` | - | MOYEN |
| **`npm install` au lieu de `npm ci`** | `apps/frontend/Dockerfile` | 10 | MOYEN |
| **ESLint desactive** (`--no-lint`) | `apps/frontend/Dockerfile` | 17 | FAIBLE |
| **Image full au lieu de slim** | `apps/api/Dockerfile` | 1 | FAIBLE |

**Scenario d'exploitation :**
1. Une image `postgres:latest` est mise a jour avec une vulnerabilite. Le prochain `docker-compose pull` l'installe silencieusement
2. Le port 5432 expose permet un acces direct a la BDD depuis l'exterieur avec les credentials `postgres/postgres`
3. Les containers root permettent une escalade de privileges en cas de container escape

**Impact :** Compromission de l'infrastructure, acces direct a la BDD, elevation de privileges

**Vraisemblance :** Elevee

**Priorite :** P1

**Correction immediate :**
- Piner toutes les images : `postgres:16.4`, `python:3.10.14-slim`, `node:20.11.1-alpine`
- Retirer l'exposition du port PostgreSQL en externe

**Correction durable :**
- Ajouter `USER appuser` dans tous les Dockerfiles
- Creer des `.dockerignore`
- Ajouter des health checks
- Scanner les images avec Trivy dans la CI

**Verification :** `docker inspect <container> | grep User` doit retourner un user non-root

---

## 2.3 Pipeline CI/CD (CircleCI)

### Problemes de securite identifies dans `.circleci/config.yml`

**Severite : ELEVEE**

| Probleme | Ligne | Severite |
|----------|-------|----------|
| **SSH sans verification de cle hote** (`StrictHostKeyChecking=no`) | 72 | CRITIQUE |
| **Images CI non pinees** (`cimg/python:3.11`) | 82, 90, 98, etc. | ELEVE |
| **Pas de scan de vulnerabilites** sur les images Docker buildees | 172-192 | ELEVE |
| **Tests de securite silencieusement ignores** (`\|\| [[ $? == 5 ]]`) | 49-50 | ELEVE |
| **Pas de SBOM** (Software Bill of Materials) | - | MOYEN |
| **Pas de signature d'images** | - | MOYEN |
| **Jobs ETL references mais Dockerfile absent** | 123-131 | MOYEN |

**Detail critique - SSH deploy (ligne 72) :**
```bash
ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP "..."
```
Desactive la verification du fingerprint SSH, rendant le deploiement vulnerable aux attaques MITM (Man-In-The-Middle).

**Detail - Tests securite ignores (lignes 49-50) :**
```bash
pytest <<parameters.app_path>>/src/tests/security/ || [[ $? == 5 ]]
```
Le code de sortie 5 (= aucun test trouve) est accepte silencieusement. Les tests de securite peuvent ne pas exister sans que la pipeline echoue.

---

## Resume Phase 2

| # | Constat | Categorie | Severite | OWASP |
|---|---------|-----------|----------|-------|
| C7 | Dependencies 100% non pinees (API), pas de lock file Python | Supply chain | ELEVEE | A06 |
| C8 | Images Docker `latest`, port BDD expose, containers root | Supply chain | ELEVEE | A08 |
| - | SSH deploy sans verification de cle hote | CI/CD | CRITIQUE | A08 |
| - | Tests securite silencieusement ignores en CI | CI/CD | ELEVE | A09 |

**Points positifs identifies :**
- Le frontend a un `package-lock.json` (builds reproductibles cote Node.js)
- L'ETL a 80% de ses dependances pinees
- Le rate limiting sur le deploy SSH est gere par CircleCI
- La pipeline a une structure de tests (unit, integration, regression, security) meme si les tests security sont vides
- Le Dockerfile frontend utilise un multi-stage build

---

## 2.4 SonarQube Cloud - Resultats

### Dashboard principal

- **Projet** : Samuel RESSIOT / EPSI_B3_MSPR-Groupe_MATS (Public, 16k lignes de code)
- **Quality Gate** : Not computed (pas d'analyse sur new code)
- **Open Issues** : 297
- **Duplications** : 1.4%
- **Coverage** : Aucune donnee (pas de tests de couverture configures)

| Metrique | Rating | Issues | Repartition severite |
|----------|--------|--------|---------------------|
| **Security** | **C** | 7 | 100% Medium |
| **Security Hotspots** | **E** | 7 (100% To Review) | 5 Medium, 2 Low |
| **Reliability** | **E** | 99 | 53% Blocker, 40% High, 1% Medium, 6% Low |
| **Maintainability** | **A** | 232 | - |

### 7 Security Issues (Vulnerabilities) - Regle python:S2068

Toutes les 7 issues concernent la meme regle : **"Credentials should not be hard-coded"** (python:S2068, CWE tagged).

| # | Fichier | Ligne | Code detecte | Classification |
|---|---------|-------|-------------|----------------|
| 1 | `apps/.../translations.py` | L13 | `"password": "Mot de passe"` | **Faux positif** - label UI francais |
| 2 | `apps/.../translations.py` | L77 | `"password": "Contraseña"` | **Faux positif** - label UI espagnol |
| 3 | `apps/.../translations.py` | L141 | `"password": "Passwort"` | **Faux positif** - label UI allemand |
| 4 | `apps/.../app/auth/db_connect...` | L23 | `os.environ.get("ETL_POSTGRES_PASSWORD", "postgres")` | **Risque securite** - fallback credential en dur |
| 5 | `apps/.../load.py` | L16 | `password="postgres"` (defaut constructeur) | **Risque securite** - credential hardcodee |
| 6 | `apps/.../loader.py` | L13 | `"password": "?"` | **Dette technique** - placeholder |
| 7 | `apps/.../src/main.py` (seeder) | L8 | `os.getenv("ADMIN_PASSWORD", "admin")` | **Risque securite** - fallback admin password |

**Analyse :**
- **3 vrais risques securite** (issues 4, 5, 7) : credentials par defaut en fallback dans le code source. Si les variables d'environnement ne sont pas definies, le systeme utilise des mots de passe triviaux (`postgres`, `admin`)
- **3 faux positifs** (issues 1, 2, 3) : SonarQube detecte le mot-cle `"password"` dans un dictionnaire de traductions UI. Ce ne sont pas des credentials mais des labels d'interface
- **1 dette technique** (issue 6) : placeholder `"?"` non fonctionnel

### 7 Security Hotspots

| # | Regle | Fichier | Ligne | Priorite | Categorie | Classification |
|---|-------|---------|-------|----------|-----------|----------------|
| 1 | **docker:S6470** | `apps/api/Dockerfile` | L7 | Medium | Permission | **Risque securite** - `COPY . .` copie potentiellement des secrets (.env, cles) dans l'image |
| 2 | **docker:S6470** | `apps/frontend/Dockerfile` | L13 | Medium | Permission | **Risque securite** - meme probleme |
| 3 | **docker:S6471** | `apps/api/Dockerfile` | L1 | Medium | Permission | **Risque securite** - `FROM python:3.10` execute en root |
| 4 | **docker:S6471** | `apps/frontend/Dockerfile` | L20 | Medium | Permission | **Risque securite** - `FROM node:20-alpine` execute en root |
| 5 | **docker:S6471** | `apps/seeder/Dockerfile` | L2 | Medium | Permission | **Risque securite** - `FROM python:3.11-slim` execute en root |
| 6 | **python:S5332** | `apps/seeder/src/main.py` | L6 | Low | Encryption | **Risque securite** - `http://api:8000` au lieu de HTTPS |
| 7 | **python:S4790** | `machine_learning_repo_in_postgres.py` | L97 | Low | Others | **Dette technique** - `hashlib.md5()` utilise pour hash de donnees (pas pour crypto) |

**Analyse :**
- **6 vrais risques securite** (hotspots 1-6) : tous lies a notre constat C8 (Docker non securise) et confirment les problemes identifies dans notre analyse manuelle
- **1 dette technique** (hotspot 7) : MD5 utilise pour hasher des valeurs en entier dans le module ML, pas pour de la cryptographie - risque faible

### 5 elements retenus pour l'audit (comme demande par le sujet)

| # | Element SonarQube | Type | Lien avec nos constats |
|---|-------------------|------|----------------------|
| 1 | **Issues 4, 5, 7** : Credentials hardcodees avec fallback (python:S2068) | Risque securite | Renforce **C5** (secrets en clair) |
| 2 | **Hotspots 3, 4, 5** : Containers Docker executent en root (docker:S6471) | Risque securite | Renforce **C8** (images Docker non securisees) |
| 3 | **Hotspots 1, 2** : `COPY . .` sans .dockerignore (docker:S6470) | Risque securite | Renforce **C8** (pas de .dockerignore) |
| 4 | **Hotspot 6** : Communication HTTP non chiffree (python:S5332) | Risque securite | Nouveau constat - lien avec **C2** (pas de HTTPS/HSTS) |
| 5 | **Reliability E** : 99 issues dont 53% Blocker | Dette technique | Non securite mais indicateur de qualite de code preoccupant |

**Elements ecartes :**
- Issues 1, 2, 3 (translations.py) : faux positifs, simples labels UI
- Issue 6 (loader.py) : placeholder non fonctionnel
- Hotspot 7 (MD5 dans ML) : usage non cryptographique, risque faible

---

## 2.5 SonarLint (IDE) - Comparaison avec SonarQube Cloud (Bonus)

### Issues detectees en local (fichiers ouverts)

| Fichier | Nb issues | Regles detectees |
|---------|-----------|-----------------|
| `apps/api/Dockerfile` | 2 | docker:S6471 (image root), docker:S6470 (COPY recursif) |
| `user_repo_in_postgres.py` | 1 | python:S108 (bloc de code vide, L57) |
| `apps/seeder/src/main.py` | 3 | python:S2068 (password hardcode), python:S112 (exception generique), python:S5332 (HTTP non securise) |
| `apps/etl/src/app/auth/db_connector.py` | 4 | python:S2068 (password), 3x python:S1066 (if statements a fusionner) |

### Ce qui est commun entre IDE et Cloud

- **Memes regles de securite detectees** : python:S2068 (credentials hardcodees), docker:S6470 (COPY recursif), docker:S6471 (containers root), python:S5332 (HTTP insecure)
- Les issues de securite sont coherentes entre les deux environnements
- SonarLint en mode connecte synchronise les regles et la configuration du Quality Profile avec SonarQube Cloud

### Ce qui differe et pourquoi

| Difference | Explication |
|-----------|-------------|
| **Scope** : Cloud analyse tout le projet (16k lignes, 297 issues), SonarLint ne montre que les fichiers ouverts | SonarLint est concu pour l'analyse en temps reel, fichier par fichier, pendant le developpement |
| **Issues supplementaires en local** : python:S108 (bloc vide), python:S112 (exception generique), python:S1066 (if a fusionner) | Ce sont des regles de maintenabilite/fiabilite que SonarLint detecte aussi mais qui ne sont pas forcement mises en avant dans le dashboard Cloud securite |
| **Temps reel vs batch** : SonarLint analyse a la frappe, Cloud necessite un push + analyse | SonarLint permet de corriger avant le commit, Cloud donne une vue globale post-push |
| **Security Hotspots** : affiches en local avec le meme detail que dans Cloud | En mode connecte, SonarLint recupere les regles de hotspots depuis le serveur Cloud |

### Conclusion

SonarLint et SonarQube Cloud sont **complementaires** :
- **SonarLint** = filet de securite en amont (pendant le developpement, temps reel)
- **SonarQube Cloud** = vue globale du projet (analyse complete, Quality Gate, suivi dans le temps)
- En mode connecte, les deux partagent la meme configuration de regles, ce qui garantit la coherence

---

## Note sur OWASP Dependency-Check

A executer manuellement :

```bash
# Via Docker :
docker run --rm -v $(pwd):/src owasp/dependency-check --scan /src --format HTML --out /src/docs/audit/
```

**Trivy (scan images Docker) :**
```bash
trivy image postgres:latest
trivy image python:3.10
trivy fs apps/api/requirements.txt
trivy fs apps/frontend/
```
