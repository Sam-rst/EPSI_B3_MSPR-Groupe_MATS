# Support de Soutenance - Audit Securite AnalyzeIT

**Module :** Security By Design - EISI I1 SECE843
**Projet audite :** AnalyzeIT - Groupe MATS
**Date :** 27 mars 2026

---

## SLIDE 1 - Contexte et perimetre (1 min)

### Le projet

AnalyzeIT est une plateforme d'analyse de donnees epidemiologiques composee de :
- **API REST** (FastAPI / Python 3.10) - 16k lignes de code
- **Frontend** (Next.js 15 / React 19)
- **ETL** (Python / Tkinter)
- **BDD** PostgreSQL + **Metabase** pour la dataviz
- **CI/CD** CircleCI + deploiement SSH sur VPS

### Donnees sensibles

- Identifiants utilisateurs (email, mot de passe)
- Tokens JWT
- Credentials admin et BDD
- Donnees epidemiologiques (donnees de sante)

### Perimetre audite

| Composant | Elements analyses |
|-----------|------------------|
| API REST | Endpoints CRUD, auth JWT, rate limiting, validation |
| Authentification | Register, login, gestion token |
| Infrastructure | Docker, CI/CD, secrets, images |
| Frontend | Headers securite, config Next.js |
| Supply chain | Dependencies Python/Node.js, images Docker |

### Cartographie des flux

```
Frontend (:3030) --JWT Bearer--> API (:8000) --SQL--> PostgreSQL (:5432)
                                    |                        |
                                 Seeder                  Metabase (:3000)

ETL (desktop) --psycopg2 + API--> PostgreSQL
```

---

## SLIDE 2 - Les 8 constats (3 min)

### 3 constats Chapitre 4 (Attaques web)

| # | Constat | OWASP | Severite | Preuve cle |
|---|---------|-------|----------|-----------|
| **C1** | Validation Pydantic insuffisante | A03 | Moyenne | Pas de `max_length`, `pattern`, `ge=0` sur les champs |
| **C2** | Zero headers securite + stack traces exposees | A05 | Elevee | `curl -D -` : aucun CSP/HSTS/X-Frame. `/docs` public. Erreurs 500 renvoient la requete SQL complete |
| **C3** | IDOR sur tous les endpoints CRUD | A01 | Critique | `DELETE /users/1` avec token user2 = 200 OK. Hash mdp dans les reponses GET |

### 3 constats Chapitre 5 (Securisation)

| # | Constat | OWASP | Severite | Preuve cle |
|---|---------|-------|----------|-----------|
| **C4** | SHA256 sans salt au lieu de bcrypt | A02 | Critique | `hashlib.sha256()` ligne 33. Hash crackable en secondes |
| **C5** | Secrets en clair + credentials par defaut | A05 | Elevee | `ADMIN_PASSWORD=Admin54321!`, fallbacks `"postgres"` en dur dans le code |
| **C6** | JWT incomplet + enumeration d'utilisateurs | A07 | Elevee | 3 messages d'erreur differents au login. Pas de refresh/blacklist/lockout |

### 2 constats Supply chain

| # | Constat | OWASP | Severite | Preuve cle |
|---|---------|-------|----------|-----------|
| **C7** | 100% deps API non pinees | A06 | Elevee | `requirements.txt` sans aucune version. Pas de lock file |
| **C8** | Docker non securise, BDD exposee | A08 | Elevee | Port 5432 ouvert, `postgres/postgres`, containers root. Crash `postgres:latest` v18 |

---

## SLIDE 3 - Top 3 des risques prioritaires (2 min)

### #1 CRITIQUE : Compromission de tous les comptes (C4 + C3)

```
Attaquant authentifie
    |
    v
GET /users/id/1  -->  reponse contient "password":"64eb837..."  (hash SHA256)
    |
    v
hashcat (GPU)  -->  SHA256 sans salt = crack en secondes
    |
    v
Acces a tous les comptes
```

**Pourquoi #1 ?** La combinaison SHA256 sans salt + hash expose dans l'API + IDOR = n'importe quel utilisateur authentifie peut compromettre tous les comptes. Zero competence technique avancee requise.

---

### #2 CRITIQUE : Acces direct a la BDD (C8 + C5)

```
Attaquant externe
    |
    v
nmap : port 5432 ouvert
    |
    v
psql -U postgres -d mspr  -->  credentials par defaut
    |
    v
SELECT * FROM "user"  -->  dump complet (hash, emails, donnees)
```

**Pourquoi #2 ?** On peut bypasser completement l'API. Le port PostgreSQL est expose avec les credentials par defaut. Demonstration concrete : le crash `postgres:latest` v18 prouve que l'infra n'est pas maitrisee.

---

### #3 ELEVE : API sans defense en profondeur (C2 + C6)

```
Attaquant
    |
    v
GET /docs  -->  cartographie complete de l'API (Swagger public)
    |
    v
POST /auth/login (test usernames)  -->  3 messages differents = enumeration
    |
    v
Erreur 500  -->  stack trace SQL : noms tables, colonnes, parametres
    |
    v
Attaque ciblee avec toutes les informations
```

**Pourquoi #3 ?** L'API fournit elle-meme toutes les informations necessaires a l'attaquant. Pas de CORS, pas de CSP, pas de HSTS, stack traces publiques.

---

## SLIDE 4 - Supply Chain : SonarQube + Dependency-Check (1 min)

### SonarQube Cloud - Dashboard

| Metrique | Rating | Detail |
|----------|--------|--------|
| Security | **C** | 7 issues (S2068 : credentials hardcodees) |
| Security Hotspots | **E** | 7 hotspots (Docker root, COPY recursif, HTTP) |
| Reliability | **E** | 99 issues (53% Blocker) |
| Maintainability | **A** | 232 issues |
| Coverage | **N/A** | Aucun test de couverture |

**5 elements retenus :**
1. Credentials hardcodees avec fallback (python:S2068) -> **Risque securite** (renforce C5)
2. Containers Docker root (docker:S6471) -> **Risque securite** (renforce C8)
3. `COPY . .` sans .dockerignore (docker:S6470) -> **Risque securite** (renforce C8)
4. HTTP non chiffre (python:S5332) -> **Risque securite** (renforce C2)
5. Reliability E (53% Blocker) -> **Dette technique**

**Ecartes :** 3 faux positifs (labels UI "password" dans traductions)

### SonarLint (IDE) vs Cloud

- **Memes regles securite** detectees des deux cotes (S2068, S6470, S6471, S5332)
- SonarLint = temps reel (pendant le dev) / Cloud = vue globale (post-push)
- Issues supplementaires en local : maintenabilite (S108, S1066, S112)

### Dependencies non pinees (C7)

- API : **10/10 dependances sans version** (aucun `==`)
- Pas de lock file Python
- **Preuve concrete** : `postgres:latest` = v18 a casse le deploy (volume incompatible)
- Frontend : OK (package-lock.json present)

---

## SLIDE 5 - Plan de securisation (2 min)

### Court terme (1-2 jours) - 7 actions

| Action | Impact |
|--------|--------|
| Remplacer SHA256 par bcrypt (12 rounds) | Elimine le risque #1 |
| Supprimer le hash password des reponses API | Elimine l'exposition |
| Uniformiser le message d'erreur login | Bloque l'enumeration |
| Fermer le port PostgreSQL en externe | Elimine le risque #2 |
| Desactiver /docs en production | Reduit la reconnaissance |
| Piner toutes les dependances + images Docker | Stabilise le deploy |
| Supprimer les fallbacks credentials hardcodes | Elimine les portes derobees |

### Moyen terme (1-2 semaines) - 7 actions

| Action | Impact |
|--------|--------|
| Middleware headers securite (CORS, CSP, HSTS) | Defense en profondeur |
| Handler d'erreur global (plus de stack traces) | Bloque la reconnaissance |
| RBAC avec verification de role par endpoint | Elimine tous les IDOR |
| USER non-root dans les Dockerfiles | Limite l'escalade de privileges |
| Validations Pydantic (max_length, pattern) | Durcit les entrees |
| Nettoyer le JWT (supprimer donnees personnelles) | RGPD / minimisation |
| pip-audit + Trivy dans la CI/CD | Detection automatique CVE |

### Structurel (1-3 mois) - 8 actions

Refresh tokens + blacklist Redis, gestionnaire de secrets (Vault), Poetry + lock file, lockout de compte, JWT en cookie HttpOnly, reverse proxy TLS, SBOM + signature images, tests securite automatises en CI.

---

## SLIDE 6 - Defense des arbitrages (reserve pour Q&A)

### Pourquoi SHA256 est critique et pas "juste moyen" ?

SHA256 est un algorithme de hachage **rapide** concu pour la verification d'integrite, pas pour les mots de passe. Un GPU moderne peut tester ~10 milliards de SHA256/seconde. Sans salt, des mots de passe identiques produisent le meme hash -> rainbow tables. Bcrypt est volontairement **lent** (ajustable via les rounds) et inclut un salt automatique.

### Pourquoi l'IDOR est critique alors que l'auth JWT fonctionne ?

L'authentification (verifier QUI est l'utilisateur) fonctionne. Mais l'autorisation (verifier CE QU'IL A LE DROIT de faire) est absente. Un utilisateur authentifie peut supprimer n'importe quel autre utilisateur. L'auth sans authz = serrure sur la porte d'entree mais pas de cles sur les coffres.

### Pourquoi le port PostgreSQL expose est critique ?

Parce qu'il permet de bypasser completement toute la securite applicative (rate limiting, JWT, validation). Acces direct = dump complet de la BDD en une commande.

### Pourquoi les faux positifs SonarQube (translations.py) ont ete ecartes ?

Les 3 issues sur `translations.py` detectent le mot-cle `"password"` comme cle d'un dictionnaire de traductions UI (`"password": "Mot de passe"`). Ce n'est pas un credential mais un label d'interface. SonarQube applique un pattern matching qui ne comprend pas le contexte semantique.

### Que dit le RGPD sur ce projet ?

Le projet manipule des donnees epidemiologiques (donnees de sante = donnees sensibles Art. 9 RGPD). Le JWT contient email/nom/prenom en clair -> violation du principe de minimisation. Le soft delete (is_deleted) peut poser un probleme de droit a l'effacement (Art. 17).

### Usage de l'IA

L'IA a ete utilisee comme assistant de recherche et d'analyse. Tous les constats ont ete **verifies par des preuves concretes** (tests curl, SonarQube, lecture du code). L'IA avait initialement suppose que le `.env` etait commite -> verifie et corrige (il ne l'etait pas). Le constat SQLi a ete reduit car l'ORM est correctement utilise.
