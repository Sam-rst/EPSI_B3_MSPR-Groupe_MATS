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

## Note sur SonarQube et OWASP Dependency-Check

Les outils SonarQube Cloud et OWASP Dependency-Check doivent etre executes manuellement par l'etudiant :

**SonarQube Cloud :**
1. Se connecter sur sonarcloud.io avec GitHub
2. Importer le depot `Sam-rst/EPSI_B3_MSPR-Groupe_MATS`
3. Lancer l'analyse sur `main`
4. Relever Quality Gate, issues et Security Hotspots
5. Selectionner 5 elements pertinents max

**OWASP Dependency-Check :**
```bash
# Installation
# Telecharger depuis https://owasp.org/www-project-dependency-check/
# Ou via Docker :
docker run --rm -v $(pwd):/src owasp/dependency-check --scan /src --format HTML --out /src/docs/audit/
```

**Trivy (scan images Docker) :**
```bash
trivy image postgres:latest
trivy image python:3.10
trivy fs apps/api/requirements.txt
trivy fs apps/frontend/
```
