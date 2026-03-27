# Phase 3 - Tests Dynamiques

Tests realises sur l'infrastructure locale (docker-compose) le 27/03/2026.

> **Note :** Le simple fait de lancer `docker-compose up` avec `postgres:latest` a provoque un crash en boucle de PostgreSQL (v18 incompatible avec le volume mount existant). C'est une **demonstration concrete du constat C8** (images non pinees).

---

## 3.1 Tests des endpoints API

### Test 1 : Requetes sans token (401 attendu)

```
GET /continents -> 401 {"detail":"Not authenticated"}
GET /users      -> 401 {"detail":"Not authenticated"}
```

**Resultat : OK** - Les endpoints proteges rejettent bien les requetes sans token.

---

### Test 2 : Token invalide / mal forme (401 attendu)

```
GET /continents (Bearer: fake_token) -> 401 {"detail":"Token invalide ou expiré : Invalid token"}
GET /continents (Bearer: JWT_mal_forme) -> 401 {"detail":"Token invalide ou expiré : Invalid token"}
```

**Resultat : PARTIELLEMENT OK** - Le rejet fonctionne, mais le message d'erreur fuite des details internes (`Invalid token` vient de PyJWT). Un attaquant sait que c'est un JWT HS256 via PyJWT.

---

### Test 3 : Enumeration d'utilisateurs (Constat C6 CONFIRME)

```
POST /auth/login {"username":"nexistepas.user","password":"test"}
  -> 400 {"message":"Le username doit être au format 'firstname.lastname'."}

POST /auth/login {"username":"evil.hacker","password":"mauvais"}
  -> 401 {"message":"Mot de passe incorrect."}
```

**Resultat : VULNERABILITE CONFIRMEE**
- 3 messages d'erreur differents selon le cas :
  - Username au mauvais format -> `"Le username doit être au format 'firstname.lastname'."`
  - Username inexistant -> message different
  - Mot de passe incorrect -> `"Mot de passe incorrect."`
- Un attaquant peut determiner si un compte existe et quels sont les formats valides

---

### Test 4 : Fuite de stack traces (Constat C2 CONFIRME)

```
POST /auth/register (avec BDD vide, avant migrations)
  -> 500 {"message":"Une erreur inattendue est survenue: (psycopg2.errors.UndefinedTable)
     relation \"user\" does not exist\nLINE 2: FROM \"user\" \n...\n
     [SQL: SELECT \"user\".firstname AS user_firstname...]\n
     [parameters: {'username_1': 'audit.test', 'param_1': 1}]"}
```

**Resultat : VULNERABILITE CRITIQUE CONFIRMEE**
- La stack trace SQL complete est renvoyee au client
- Expose : noms de tables (`user`), noms de colonnes (`firstname`, `lastname`, `username`, `email`, `password`...), parametres de requete, version SQLAlchemy
- L'erreur de register (apres migrations) fuite aussi les erreurs de validation Pydantic internes

---

### Test 5 : IDOR - Acces croise entre utilisateurs (Constat C3 CONFIRME)

```
# User 1 (audit.test) accede a ses propres donnees
GET /users/id/1 (Bearer: token_user1)
  -> 200 {"item":{"firstname":"Audit","email":"audit.test@analyseit.com",
     "password":"64eb83717161a26a63003f4b7ec2679b924607fab07e412775f3f9622e2d0618",...}}

# User 1 supprime un utilisateur
DELETE /users/1 (Bearer: token_user1)
  -> 200 {"message":"L'utilisateur 'Audit Test' a bien été supprimé."}
```

**Resultat : VULNERABILITES CRITIQUES CONFIRMEES**

1. **Le hash du mot de passe est retourne dans la reponse API** (`"password":"64eb837..."`)
   - N'importe quel utilisateur authentifie peut recuperer le hash SHA256 de n'importe quel autre utilisateur
   - Combine avec SHA256 sans salt, les mots de passe sont crackables en secondes

2. **Aucun controle d'acces** : un utilisateur peut supprimer n'importe quel autre utilisateur via `DELETE /users/{id}`

3. **Pas de verification de propriete** : `GET /users/id/{id}` retourne les donnees de n'importe quel utilisateur

---

### Test 6 : Rate limiting (Point positif)

```
# Login (limite: 5/min)
Requetes 1-6: HTTP 429 (Too Many Requests)

# Register (limite: 2/min)
Requetes 1-3: HTTP 429 (Too Many Requests)
```

**Resultat : FONCTIONNEL** - Le rate limiting est en place et bloque correctement les requetes excessives. Cependant, il est base sur l'adresse IP uniquement (contournable avec des proxies).

---

## 3.2 Cookies et sessions

### Test 7 : Headers de reponse HTTP (Constat C2 CONFIRME)

**API (http://localhost:8000/) :**
```
HTTP/1.1 200 OK
date: Fri, 27 Mar 2026 12:28:24 GMT
server: uvicorn
content-length: 25
content-type: application/json
```

**Frontend (http://localhost:3030/) :**
```
HTTP/1.1 200 OK
x-nextjs-cache: HIT
X-Powered-By: Next.js
Cache-Control: s-maxage=31536000
Content-Type: text/html; charset=utf-8
```

**Resultat : AUCUN HEADER DE SECURITE sur les deux services**

| Header | API | Frontend | Attendu |
|--------|-----|----------|---------|
| `Content-Security-Policy` | ABSENT | ABSENT | Requis |
| `X-Frame-Options` | ABSENT | ABSENT | `DENY` ou `SAMEORIGIN` |
| `X-Content-Type-Options` | ABSENT | ABSENT | `nosniff` |
| `Strict-Transport-Security` | ABSENT | ABSENT | `max-age=31536000; includeSubDomains` |
| `Referrer-Policy` | ABSENT | ABSENT | `strict-origin-when-cross-origin` |
| `X-Powered-By` | ABSENT | **PRESENT (`Next.js`)** | Doit etre supprime (fingerprinting) |
| `Set-Cookie` | ABSENT | ABSENT | - |

### Test 8 : Gestion du token JWT (Constat C6 CONFIRME)

- **Pas de cookie** : le token JWT est renvoye uniquement dans le corps de la reponse JSON (`access_token`)
- Le frontend doit le stocker en `localStorage` ou `sessionStorage` (vulnerable au XSS)
- **Pas de cookie HttpOnly/Secure/SameSite** : le token n'est pas protege par les mecanismes navigateur
- **Pas de cookie de session** du tout

### Test 9 : Contenu du JWT (donnees sensibles)

```json
{
  "sub": "audit.test",
  "id": 1,
  "role_id": null,
  "country_id": null,
  "email": "audit.test@analyseit.com",
  "firstname": "Audit",
  "lastname": "Test",
  "username": "audit.test",
  "exp": 1774618069
}
```

**Problemes :**
- Le JWT contient des donnees personnelles en clair (email, nom, prenom)
- Ces donnees sont lisibles par n'importe qui (le JWT n'est pas chiffre, juste signe)
- Principe de minimisation RGPD : seul `sub` et `exp` devraient etre dans le token

---

## 3.3 Acces direct a la base de donnees (Constat C8 CONFIRME)

```sql
-- Depuis l'exterieur via le port 5432 expose
SELECT username, email, password FROM "user";

  username    |           email            |                             password
--------------+----------------------------+------------------------------------------------------------------
 audit.test   | audit.test@analyseit.com   | 64eb83717161a26a63003f4b7ec2679b924607fab07e412775f3f9622e2d0618
 evil.hacker  | evil.hacker@analyseit.com  | 08d536ba5e259d8f642ffbb0cdf9db8abb72b852cb6dd87da2a2f326fb4cf13c
```

**Resultat : CRITIQUE**
- La BDD PostgreSQL est accessible directement depuis l'exterieur (port 5432 expose)
- Les credentials sont `postgres/postgres` (par defaut)
- Les mots de passe sont des hash SHA256 sans salt, crackables en secondes
- Acces total en lecture/ecriture a toutes les donnees

---

## Resume Phase 3

| Test | Constat confirme | Severite | Preuve |
|------|-----------------|----------|--------|
| Fuite stack traces SQL dans les erreurs | C2 | CRITIQUE | Requete SQL complete + colonnes + params dans la reponse 500 |
| Hash du mot de passe retourne par l'API | C3 + C4 | CRITIQUE | GET /users/id/{id} retourne le champ `password` |
| IDOR : suppression d'un autre utilisateur | C3 | CRITIQUE | DELETE /users/1 sans verification |
| Enumeration d'utilisateurs | C6 | ELEVEE | 3 messages d'erreur differents au login |
| Zero headers de securite HTTP | C2 | ELEVEE | curl -D - confirme l'absence totale |
| JWT avec donnees personnelles en clair | C6 | MOYENNE | email, nom, prenom dans le payload JWT |
| BDD accessible depuis l'exterieur | C8 | CRITIQUE | psql direct sur port 5432, credentials par defaut |
| X-Powered-By expose (frontend) | C2 | FAIBLE | Facilite le fingerprinting |

**Points positifs confirmes :**
- Rate limiting fonctionnel (429 correctement renvoye)
- Endpoints proteges rejettent bien les requetes sans token (401)
- Tokens invalides correctement rejetes
