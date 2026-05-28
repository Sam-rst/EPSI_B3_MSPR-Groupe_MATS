# Soutenance - Defense du plan de securisation AnalyzeIT

**Module :** Security By Design - EISI I1 SECE843
**Projet :** AnalyzeIT - Groupe MATS
**Date :** 27 mars 2026
**Présenté par :** Samuel RESSIOT et Yassine ZOUITNI


---

## SLIDE 1 - Contexte et perimetre

### Le projet

AnalyzeIT : plateforme d'analyse de donnees epidemiologiques

| Composant | Technologie | Role |
|-----------|-------------|------|
| API REST | FastAPI / Python 3.10 | Backend, endpoints CRUD, auth JWT |
| Frontend | Next.js 15 / React 19 | Interface web (port 3030) |
| ETL | Python / Tkinter | Import de donnees (desktop) |
| BDD | PostgreSQL | Stockage persistant |
| Dataviz | Metabase | Tableaux de bord |
| CI/CD | CircleCI | Lint, tests, deploy SSH |
| Infra | Docker Compose | Orchestration des services |

### Donnees sensibles manipulees

- Identifiants utilisateurs (email, mot de passe)
- Tokens JWT (session)
- Credentials admin et BDD
- Donnees epidemiologiques (donnees de sante - Art. 9 RGPD)

### Perimetre audite

API REST (endpoints, auth, rate limiting), authentification (register, login, JWT), infrastructure (Docker, CI/CD, secrets, images), frontend (headers), supply chain (dependencies Python/Node.js, images Docker)

### Rappel : 8 constats identifies lors de l'audit

| # | Constat | Severite |
|---|---------|----------|
| C1 | Validation Pydantic insuffisante | Moyenne |
| C2 | Zero headers securite + stack traces exposees | Elevee |
| C3 | IDOR : aucun controle d'acces | **Critique** |
| C4 | SHA256 sans salt au lieu de bcrypt | **Critique** |
| C5 | Secrets en clair + credentials par defaut | Elevee |
| C6 | JWT incomplet + enumeration utilisateurs | Elevee |
| C7 | 100% dependencies API non pinees | Elevee |
| C8 | Docker non securise, BDD exposee | Elevee |

---

## SLIDE 2 - Top 3 des risques majeurs

### #1 CRITIQUE : Compromission de tous les comptes (C4 + C3)

```
Utilisateur authentifie
    → GET /users/id/1
    → Reponse : "password":"64eb837..." (hash SHA256)
    → hashcat GPU : crack en secondes (SHA256 sans salt)
    → Acces a TOUS les comptes
```

**Justification du classement :** SHA256 sans salt + hash expose via l'API + IDOR = compromission totale, zero competence avancee requise. C'est la faille la plus critique car elle combine 3 vulnerabilites en une chaine d'attaque triviale.

### #2 CRITIQUE : Acces direct a la BDD (C8 + C5)

```
Attaquant externe
    → nmap : port 5432 ouvert
    → psql -U postgres (credentials par defaut)
    → SELECT * FROM "user" → dump complet
```

**Justification :** Bypass complet de toute la securite applicative. Preuve concrete : le crash `postgres:latest` v18 demontre que l'infra n'est pas maitrisee.

### #3 ELEVE : API sans defense en profondeur (C2 + C6)

```
Attaquant
    → GET /docs → Swagger public (cartographie complete)
    → POST /auth/login → 3 messages differents = enumeration
    → Erreur 500 → requete SQL complete exposee
```

**Justification :** L'API fournit toutes les informations necessaires pour planifier une attaque ciblee. Aucune couche de protection (pas de CORS, CSP, HSTS).

---

## SLIDE 3 - Correction 1 : Code applicatif / Controle d'acces

**Constats traites :** C3 (IDOR) + C4 (hash expose)
**Nature :** Code applicatif / Controle d'acces

### AVANT

```python
# GET /users/id/1 retourne le hash du mot de passe
content = {"item": jsonable_encoder(user)}
# → {"id": 1, "username": "...", "password": "64eb837...", ...}

# DELETE /users/1 avec le token de user2 → 200 OK (aucune verification)
user = usecase.execute(id)
```

### APRES

```python
# Champs sensibles exclus de toutes les reponses
SENSITIVE_FIELDS = {"password", "password_hash"}
content = {"item": jsonable_encoder(user, exclude=SENSITIVE_FIELDS)}
# → {"id": 1, "username": "...", "email": "..."}  (PAS de password)

# Verification d'ownership avant suppression
if current_user.get("id") != id and current_user.get("role_id") != 1:
    return JSONResponse(status_code=403, content={"message": "Acces non autorise"})
```

### VALIDATION

| Verification | Methode | Resultat |
|-------------|---------|----------|
| Champ password absent des reponses | `grep "exclude=SENSITIVE" router.py` | 3 endpoints proteges (GET all, by_id, by_username) |
| IDOR bloque sur DELETE | `grep "current_user.*role_id" router.py` | Check ownership present |
| hashlib.sha256 absent du user repo | `grep "hashlib.sha256" apps/api/` | 0 match |

**Fichier modifie :** `apps/api/src/app/user/presentation/router.py`

---

## SLIDE 4 - Correction 2 : Configuration securite / Headers

**Constats traites :** C2 (headers, stack traces, /docs)
**Nature :** Configuration de securite / Headers

### AVANT

```bash
curl -I http://localhost:8000/
# → Aucun header de securite (0 CSP, 0 HSTS, 0 X-Frame-Options)

curl http://localhost:8000/docs
# → 200 OK (Swagger complet expose a tous)

# Erreur 500 → "detail": "SELECT * FROM user WHERE..." (stack trace SQL)
```

### APRES

```python
# Nouveau middleware : 7 headers de securite sur chaque reponse
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        # + X-XSS-Protection, Referrer-Policy, Permissions-Policy

# /docs desactive en production
app = FastAPI(docs_url=None if is_prod else "/docs", ...)

# Error handler global : plus de stack traces
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Erreur interne: {exc}", exc_info=True)  # log interne
    return JSONResponse(status_code=500,
        content={"message": "Une erreur interne est survenue."})  # message generique
```

### VALIDATION

| Verification | Methode | Resultat |
|-------------|---------|----------|
| 7 headers de securite | Lecture `security_headers.py` | CSP, HSTS, X-Frame, X-Content-Type, X-XSS, Referrer, Permissions |
| /docs desactive en prod | `grep "docs_url.*None" main.py` | Conditionnel sur `ENV=production` |
| Error handler global | `grep "global_exception_handler" main.py` | Present + log interne |
| CORS active | `grep "CORSMiddleware" main.py` | Whitelist depuis env var |

**Fichiers :** `apps/api/src/main.py` + `apps/api/src/core/middlewares/security_headers.py` (nouveau)

---

## SLIDE 5 - Correction 3 : Authentification / Secrets

**Constats traites :** C4 (SHA256) + C5 (secrets hardcodes) + C6 (enumeration)
**Nature :** Authentification, secrets, exposition technique

### AVANT

```python
# Hachage SHA256 sans salt (crackable en secondes)
password_hashed = hashlib.sha256(payload.password.encode()).hexdigest()
# → "64eb837..." (64 chars hex, pas de salt, GPU: 10 milliards/sec)

# Verification non constante en temps (timing attack)
return user.password == password_hashed

# 3 messages d'erreur differents → enumeration d'utilisateurs
"Le username doit etre au format 'firstname.lastname'."
"Le username n'existe pas."
"Mot de passe incorrect."

# Fallbacks de credentials hardcodes dans le code
os.getenv("ADMIN_PASSWORD", "admin")           # seeder
os.environ.get("ETL_POSTGRES_PASSWORD", "postgres")  # ETL
```

### APRES

```python
# bcrypt 12 rounds avec salt automatique
password_hashed = bcrypt.hashpw(
    payload.password.encode(), bcrypt.gensalt(rounds=12)
).decode()
# → "$2b$12$K8GpQzL..." (60 chars, salt inclus, volontairement lent)

# Verification en temps constant (anti timing attack)
return bcrypt.checkpw(password_to_verify.encode(), user.password.encode())

# Message unique pour les 3 cas (anti-enumeration)
invalid_credentials_msg = "Identifiants invalides."

# Plus de fallbacks : KeyError si non defini
os.environ["ADMIN_PASSWORD"]           # crash si absent
os.environ["ETL_POSTGRES_PASSWORD"]    # crash si absent
```

### VALIDATION

| Verification | Methode | Resultat |
|-------------|---------|----------|
| bcrypt 12 rounds | `grep "bcrypt" user_repo_in_postgres.py` | hashpw + gensalt(rounds=12) + checkpw |
| Message unique login | `grep "n'existe pas\|incorrect" login_usecase.py` | 0 match (supprimes) |
| Fallbacks supprimes | `grep "getenv.*admin\|get.*postgres" apps/` | 0 match dans seeder/ETL |
| bcrypt dans deps | `grep "bcrypt" requirements.txt` | Present |

**6 fichiers modifies** : user_repo, login_usecase, requirements.txt, db_connector, load.py, seeder/main.py

---

## SLIDE 6 - Plan de securisation final et arbitrages

### Immediat - corrige aujourd'hui (8/8)

| # | Action | Statut |
|---|--------|--------|
| 1 | Masquer password dans les reponses API | Fait |
| 2 | Verification ownership sur DELETE (IDOR) | Fait |
| 3 | Middleware 7 headers de securite | Fait |
| 4 | Desactiver /docs en production | Fait |
| 5 | Error handler global (plus de stack traces) | Fait |
| 6 | SHA256 → bcrypt 12 rounds | Fait |
| 7 | Supprimer fallbacks credentials hardcodes | Fait |
| 8 | Uniformiser message d'erreur login | Fait |

### Moyen terme (1-2 semaines)

| Action | Arbitrage |
|--------|-----------|
| RBAC complet par endpoint | Necessite refonte des usecases - trop lourd pour une session |
| Piner deps + images Docker | Pipeline CI/CD a adapter |
| USER non-root dans Dockerfiles | Tests staging necessaires |
| Validations Pydantic | Impact API contract existant |
| JWT minimal (supprimer email/nom) | Impact frontend a evaluer |
| pip-audit + Trivy en CI | Config CircleCI a adapter |
| Fermer port PostgreSQL en externe | Impact dev local a gerer |

### Structurel (1-3 mois)

Refresh tokens + blacklist Redis | Vault/Docker Secrets | Poetry + lock file | Lockout compte | JWT cookie HttpOnly | Reverse proxy TLS | SBOM + signature images | Tests securite CI

### Arbitrages defendus

- **Pourquoi IDOR seulement sur users ?** Le RBAC complet (20+ endpoints) necessite une refonte des usecases. On traite le cas le plus critique (users = donnees personnelles). Le reste est planifie moyen terme.
- **Pourquoi le port 5432 reste expose ?** Necessaire en dev local. Sera ferme en staging/prod via `docker-compose.prod.yml`. Le risque est documente.
- **Pourquoi pas de lockout ?** Risque de DoS par lockout massif sans solution anti-bot. Le rate limiting (5/min) est la mesure compensatoire retenue.

---

## SLIDE 7 - Risque residuel et conclusion operationnelle

### Bilan chiffre

| Metrique | Avant | Apres |
|----------|-------|-------|
| Constats critiques | 2 | **0** |
| Constats eleves | 5 | **2 restants** (C7, C8 partiels) |
| Constats moyens | 1 | 1 (inchange) |
| Actions immediates | 0/8 | **8/8** |
| Headers de securite | 0 | **7** |
| Fallbacks hardcodes | 3 fichiers | **0** |

### Ce qui est corrige

- Compromission des comptes eliminee (bcrypt + champ masque + ownership)
- Defense en profondeur de l'API (7 headers, /docs ferme, stack traces masquees, CORS)
- Enumeration d'utilisateurs bloquee (message unique)
- Secrets hardcodes supprimes (crash si absent)

### Ce qui reste a traiter

- IDOR sur les autres entites (epidemics, vaccines...) → RBAC complet (moyen terme)
- Dependencies non pinees (C7) → Poetry + lock file
- Containers root + port 5432 (C8) → docker-compose.prod.yml

### Ce qui est accepte temporairement

- JWT en body (pas en cookie HttpOnly) → rate limiting en place, token 1h
- Pas de refresh token → re-login toutes les heures, acceptable pour usage interne
- Port 5432 en dev local → bloque en staging/prod
- Valeurs pre-remplies `"postgres"` dans GUI ETL → visible, modifiable par l'utilisateur

### Conclusion operationnelle

Les 3 corrections implementees eliminent les 2 constats critiques et traitent 5 des 8 constats identifies. Le plan immediat est 100% execute. Les actions restantes sont planifiees et priorisees avec des arbitrages documentes. Le projet passe d'un niveau de risque **critique** a un niveau **modere** avec des mesures compensatoires en place.
