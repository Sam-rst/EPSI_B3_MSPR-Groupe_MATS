# Phase 1 - Analyse Statique du Code

## 1.1 Secrets et configuration

### Constat C5 : Gestion des secrets (Chapitre 5 - Seance 5)

**Severite : ELEVEE**

**Preuve :**
- Le fichier `.env` est bien dans `.gitignore` et n'a jamais ete commite dans l'historique Git
- Cependant, les fichiers `config/env/dev.conf` et `config/env/prod.conf` sont commites et contiennent `DEBUG=True` / `DEBUG=False` en dur
- Le `.env` local contient en clair :
  - `JWT_SECRET_KEY=gWUD/LVgaeLVQf6o8rLmC7zN7lqut6rEY23Ooga+eXw=`
  - `ADMIN_PASSWORD=Admin54321!`
  - `SONAR_TOKEN=sqa_b1b16689dc74c46577b4b575a82f31d853fac15b`
  - `MB_DB_PASS=METABASEmspr2025!`
  - `POSTGRES_PASSWORD=postgres`
- Pas de rotation des secrets, pas de gestionnaire de secrets (Vault, AWS Secrets Manager)
- Le mot de passe admin par defaut `Admin54321!` est faible et previsible

**Scenario d'exploitation :**
Un developpeur quittant l'equipe conserve les credentials. Le mot de passe admin etant faible et non change, il peut acceder au systeme.

**Impact :** Compromission complete du systeme (acces admin, BDD, JWT forgeable)

**Vraisemblance :** Elevee (credentials en dur, pas de rotation)

**Priorite :** P1

**Correction immediate :** Regenerer tous les secrets, utiliser des mots de passe forts generes aleatoirement

**Correction durable :** Mettre en place un gestionnaire de secrets (Vault, Docker Secrets). Implementer une rotation automatique

**Verification :** Verifier qu'aucun secret ne figure dans les fichiers commites via `gitleaks`

---

## 1.2 Authentification

### Constat C4 : Hashage des mots de passe SHA256 au lieu de bcrypt (Chapitre 5 - Seance 5)

**Severite : CRITIQUE**

**Preuve :**
- Fichier : `apps/api/src/app/user/infrastructure/repository/user_repo_in_postgres.py`
- Ligne 3 : `import hashlib`
- Ligne 33 : `password_hashed = hashlib.sha256(payload.password.encode()).hexdigest()`
- Ligne 126 : `password_hashed = hashlib.sha256(password_to_verify.encode()).hexdigest()`
- Aucune dependance bcrypt ou argon2 dans `requirements.txt`
- SHA256 est un algorithme rapide sans sel (salt) : vulnerable au brute-force GPU

**Scenario d'exploitation :**
En cas de fuite de la BDD, un attaquant peut casser les mots de passe SHA256 en quelques secondes avec un GPU moderne (hashcat/john). SHA256 sans salt = mots de passe identiques produisent le meme hash.

**Impact :** Compromission de tous les comptes utilisateurs

**Vraisemblance :** Elevee si fuite de BDD (pas de defense en profondeur)

**Priorite :** P1

**Correction immediate :** Remplacer `hashlib.sha256` par `bcrypt.hashpw()` avec 12 rounds minimum

**Correction durable :** Ajouter `bcrypt` ou `argon2-cffi` aux dependances. Migrer les hash existants (re-hash au prochain login)

**Verification :** Verifier que les hash en BDD commencent par `$2b$` (bcrypt) et non un hash SHA256 de 64 caracteres hex

---

### Constat C6 : Gestion JWT incomplete et failles d'authentification (Chapitre 5 - Seance 5)

**Severite : ELEVEE**

**Preuves multiples :**

**a) Enumeration d'utilisateurs via messages d'erreur differents**
- Fichier : `apps/api/src/app/auth/application/usecase/login_user_usecase.py`
- Ligne 52-56 : `detail="Le username n'existe pas."` (revele que le username est invalide)
- Ligne 59-63 : `detail="Mot de passe incorrect."` (revele que le username est valide)
- Un attaquant peut enumerer les comptes existants en testant des usernames

**b) Pas de mecanisme de refresh token**
- Fichier : `apps/api/src/core/auth/authorizer.py` - seul `create_access_token()` existe
- `JWT_REFRESH_TOKEN_EXPIRES` est defini dans `settings.py` (ligne 48) mais jamais utilise
- Token d'acces de 1h sans refresh = mauvaise UX et securite

**c) Pas de revocation de token (blacklist)**
- `JWT_BLACKLIST_ENABLED` est defini dans `settings.py` (ligne 49) mais jamais implemente
- Impossible d'invalider un token vole ou apres changement de mot de passe

**d) Pas de verrouillage de compte**
- Aucun suivi des tentatives de connexion echouees
- Pas de lockout apres N echecs

**e) Vulnerabilite aux attaques temporelles (timing attack)**
- Fichier : `user_repo_in_postgres.py`, ligne 126
- Comparaison directe `user.password == password_hashed` au lieu de `hmac.compare_digest()`

**f) Pas de validation de complexite du mot de passe**
- Fichier : `apps/api/src/app/auth/presentation/model/payload/register_payload.py`
- Le champ `password` n'a aucune contrainte (longueur, complexite)

**Scenario d'exploitation :**
1. L'attaquant enumere les comptes via les messages d'erreur
2. Brute-force le mot de passe sans lockout (5 req/min via rate limit, mais pas de lockout)
3. Token obtenu non revocable pendant 1h

**Impact :** Acces non autorise aux comptes, pas de defense contre le vol de token

**Vraisemblance :** Moyenne a elevee

**Priorite :** P1

**Correction immediate :** Uniformiser les messages d'erreur : `"Identifiants invalides."`

**Correction durable :** Implementer refresh token, blacklist, lockout apres 5 echecs, `hmac.compare_digest()`

**Verification :** Tester que les reponses de login sont identiques que le username existe ou non

---

## 1.3 Validation des entrees

### Constat C1 : Validation insuffisante des entrees Pydantic (Chapitre 4 - Seance 4)

**Severite : MOYENNE**

**Preuve :**
- Tous les modeles Pydantic manquent de contraintes de validation :
  - `apps/api/src/app/auth/presentation/model/payload/login_payload.py` : `username` et `password` sans `max_length`
  - `apps/api/src/app/country/presentation/model/payload/create_country_payload.py` : `iso2`, `iso3` sans pattern regex
  - `apps/api/src/app/epidemic/presentation/model/payload/create_epidemic_payload.py` : pas de validation `end_date >= start_date`
  - `apps/api/src/app/continent/presentation/model/payload/create_continent_payload.py` : `population` peut etre negatif
- Le modele `FilterRequest` (`apps/api/src/app/base/presentation/model/payload/base_payload.py`, lignes 57-86) accepte des noms de colonnes et modeles arbitraires sans whitelist

**Point positif :** L'ORM SQLAlchemy est utilise partout, pas de requetes SQL brutes. Le risque d'injection SQL directe est faible.

**Scenario d'exploitation :**
Envoi de payloads avec des champs excessivement longs (DoS), populations negatives corrompant les donnees, ou manipulation du `FilterRequest` pour acceder a des colonnes non prevues.

**Impact :** Corruption de donnees, DoS potentiel

**Vraisemblance :** Moyenne

**Priorite :** P2

**Correction immediate :** Ajouter `max_length`, `min_length`, `ge=0` sur les champs critiques

**Correction durable :** Creer des types Pydantic reutilisables (ex: `ISOCode`, `PositivePopulation`) et une whitelist pour `FilterRequest`

**Verification :** Tester avec des payloads malformes via curl/Postman

---

### Constat C3 : Absence de controle d'acces (IDOR) (Chapitre 4 - Seance 4)

**Severite : ELEVEE**

**Preuve :**
- Tous les endpoints CRUD ne verifient pas que l'utilisateur a le droit d'acceder/modifier la ressource
- Exemples :
  - `GET /users/id/{id}` : n'importe quel utilisateur authentifie peut lire les donnees d'un autre
  - `DELETE /users/{id}` : n'importe qui peut supprimer un autre utilisateur
  - `PATCH /countries/{id}`, `DELETE /epidemics/{id}`, etc. : aucune verification de role
- Les usecases ne recoivent que l'`id` de la ressource, jamais le contexte utilisateur
- Exemple dans `apps/api/src/app/country/application/usecase/find_country_by_id_usecase.py` (lignes 12-26) : pas de parametre user, pas de verification d'autorisation
- Il existe une entite `Role` mais aucun RBAC n'est implemente

**Scenario d'exploitation :**
Un utilisateur authentifie modifie l'ID dans l'URL (`/users/id/1` -> `/users/id/2`) pour acceder aux donnees d'un autre utilisateur ou les supprimer.

**Impact :** Acces non autorise, modification/suppression de donnees d'autres utilisateurs

**Vraisemblance :** Elevee (trivial a exploiter)

**Priorite :** P1

**Correction immediate :** Ajouter une verification `current_user.role` avant chaque operation d'ecriture

**Correction durable :** Implementer un middleware RBAC avec des permissions par endpoint. Utiliser les roles existants en BDD

**Verification :** Tester avec 2 comptes differents : un user ne doit pas pouvoir DELETE un autre user

---

## 1.4 Headers de securite HTTP

### Constat C2 : Absence totale de headers de securite et CORS (Chapitre 4 - Seance 4)

**Severite : ELEVEE**

**Preuve :**
- Fichier : `apps/api/src/main.py` - **Aucun CORSMiddleware configure**
- Les variables CORS existent dans `apps/api/src/config/config.py` (lignes 39-44) mais ne sont **jamais utilisees**
- Aucun des headers de securite suivants n'est configure :
  - `Content-Security-Policy` (CSP)
  - `X-Frame-Options`
  - `X-Content-Type-Options`
  - `Strict-Transport-Security` (HSTS)
  - `Referrer-Policy`
- Swagger/docs expose inconditionnellement : `apps/api/src/main.py` ligne 19 : `FastAPI(docs_url="/docs")`
- `DEBUG=True` en configuration dev (et le `.env` utilise cette valeur)
- Frontend Next.js : `apps/frontend/next.config.mjs` ne configure aucun header de securite
- 49+ fichiers exposent les stack traces dans les reponses d'erreur via `detail=f"...{str(e)}"`

**Scenario d'exploitation :**
1. Clickjacking : l'API peut etre embedee dans un iframe malveillant (pas de `X-Frame-Options`)
2. XSS : pas de CSP pour bloquer les scripts injectes
3. Reconnaissance : `/docs` expose toute la structure de l'API publiquement
4. Les messages d'erreur detailles revelent des chemins internes et la stack technique

**Impact :** Surface d'attaque elargie, facilite la reconnaissance et l'exploitation

**Vraisemblance :** Elevee

**Priorite :** P1

**Correction immediate :** Ajouter un middleware FastAPI avec les headers de securite essentiels. Desactiver `/docs` en production

**Correction durable :** Configurer CORS avec whitelist stricte (`allow_origins=["http://localhost:3030"]`). Ajouter CSP, HSTS, X-Frame-Options. Implementer un handler d'erreur global qui ne fuite pas les details

**Verification :** `curl -I http://localhost:8000/` et verifier la presence des headers

---

## Resume Phase 1

| # | Constat | Chapitre | Severite | Priorite | OWASP |
|---|---------|----------|----------|----------|-------|
| C4 | SHA256 au lieu de bcrypt | Chap 5 | CRITIQUE | P1 | A02 |
| C3 | IDOR - pas de controle d'acces | Chap 4 | ELEVEE | P1 | A01 |
| C2 | Pas de CORS, pas de headers securite | Chap 4 | ELEVEE | P1 | A05 |
| C6 | JWT sans refresh/blacklist, enumeration users | Chap 5 | ELEVEE | P1 | A07 |
| C5 | Secrets en clair, pas de rotation | Chap 5 | ELEVEE | P1 | A05 |
| C1 | Validation Pydantic insuffisante | Chap 4 | MOYENNE | P2 | A03 |

**Points positifs identifies :**
- SQLAlchemy ORM utilise partout (pas d'injection SQL directe)
- Rate limiting en place sur les endpoints sensibles (register: 2/min, login: 5/min)
- Soft delete implemente (tracabilite)
- Audit trail sur les entites (created_by, updated_by)
