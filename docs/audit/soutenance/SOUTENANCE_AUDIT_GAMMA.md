# Prompt Gamma - Audit Securite AnalyzeIT

## Instructions pour Gamma

> Coller ce contenu dans Gamma (gamma.app) > "Paste in text" ou "Generate from text".
> Style : sombre/tech, minimaliste. Pas de phrases completes, uniquement des mots-cles et tableaux.
> 8 slides max. Police sans-serif. Icones si possible.

---

## Slide 1 : Page de titre

**Audit Securite Approfondi - AnalyzeIT**

Security By Design - EISI I1 SECE843

Groupe MATS - Mars 2026

---

## Slide 2 : Contexte et perimetre

**AnalyzeIT** - Plateforme d'analyse de donnees epidemiologiques

Stack technique :
- API REST : FastAPI / Python 3.10
- Frontend : Next.js 15 / React 19
- BDD : PostgreSQL
- Dataviz : Metabase
- CI/CD : CircleCI
- Infra : Docker Compose

Donnees sensibles : identifiants utilisateurs, tokens JWT, credentials admin, donnees de sante

Perimetre : API, authentification, infrastructure Docker, supply chain, frontend

Schema des flux :

```
Frontend (:3030) → API (:8000) → PostgreSQL (:5432)
                       ↓                 ↓
                    Seeder          Metabase (:3000)
ETL (desktop) → PostgreSQL
```

---

## Slide 3 : 8 constats de securite identifies

### Chapitre 4 - Attaques web

| Constat | OWASP | Severite |
|---------|-------|----------|
| C1 - Validation entrees insuffisante | A03 | Moyenne |
| C2 - Zero headers securite, stack traces exposees | A05 | Elevee |
| C3 - IDOR : aucun controle d'acces | A01 | Critique |

### Chapitre 5 - Securisation

| Constat | OWASP | Severite |
|---------|-------|----------|
| C4 - SHA256 sans salt (pas bcrypt) | A02 | Critique |
| C5 - Secrets en clair, credentials par defaut | A05 | Elevee |
| C6 - JWT incomplet, enumeration utilisateurs | A07 | Elevee |

### Supply chain

| Constat | OWASP | Severite |
|---------|-------|----------|
| C7 - 100% deps API non pinees | A06 | Elevee |
| C8 - Docker non securise, BDD exposee | A08 | Elevee |

---

## Slide 4 : Top 3 risques - #1 Compromission des comptes

**Risque #1 : SHA256 + IDOR (C4 + C3)**

Severite : CRITIQUE

Chaine d'attaque :
1. Utilisateur authentifie
2. GET /users/id/1 → hash SHA256 dans la reponse
3. Hashcat GPU → crack en secondes
4. Acces a tous les comptes

Preuve : `"password":"64eb83717161a26a..."` retourne par l'API

Pourquoi critique : zero competence technique avancee requise

---

## Slide 5 : Top 3 risques - #2 et #3

**Risque #2 : BDD exposee (C8 + C5)**

Chaine d'attaque :
1. Scan port 5432 ouvert
2. psql -U postgres → credentials par defaut
3. SELECT * FROM "user" → dump complet

Preuve concrete : crash postgres:latest v18 au deploy

**Risque #3 : API sans defense (C2 + C6)**

Chaine d'attaque :
1. /docs → cartographie complete (Swagger public)
2. Login → 3 messages differents = enumeration
3. Erreur 500 → requete SQL complete exposee

---

## Slide 6 : SonarQube + Supply Chain

### Dashboard SonarQube Cloud

| Metrique | Rating |
|----------|--------|
| Security | C (7 issues) |
| Hotspots | E (7 hotspots, 0% reviewed) |
| Reliability | E (99 issues, 53% Blocker) |
| Maintainability | A |
| Coverage | N/A |

5 elements retenus : credentials hardcodees, containers root, COPY sans .dockerignore, HTTP non chiffre, reliability E

3 faux positifs ecartes : labels UI "password" dans traductions

### SonarLint vs Cloud
- Memes regles securite detectees
- IDE = temps reel / Cloud = vue globale

### Dependencies
- API : 10/10 non pinees, pas de lock file
- Preuve : postgres:latest v18 = crash deploy

---

## Slide 7 : Plan de securisation

### Court terme (1-2 jours)

| Action | Risque elimine |
|--------|---------------|
| SHA256 → bcrypt 12 rounds | #1 |
| Supprimer hash des reponses API | #1 |
| Uniformiser erreur login | #3 |
| Fermer port 5432 | #2 |
| Desactiver /docs en prod | #3 |
| Piner deps + images Docker | Supply chain |
| Supprimer fallbacks credentials | #2 |

### Moyen terme (1-2 semaines)

Headers securite (CORS, CSP, HSTS) · Handler erreur global · RBAC par endpoint · USER non-root Docker · Validations Pydantic · JWT minimal · pip-audit + Trivy en CI

### Structurel (1-3 mois)

Refresh tokens + blacklist · Vault · Poetry lock · Lockout compte · Cookie HttpOnly · Reverse proxy TLS · SBOM · Tests securite CI

---

## Slide 8 : Usage de l'IA et conclusion

### Usage de l'IA

| Aspect | Detail |
|--------|--------|
| Propose | Analyse code parallele, mapping OWASP, commandes curl, structure rapports |
| Garde | Tous les constats confirmes par preuves concretes |
| Rejete | .env suppose commite → verifie : non (gitignore OK). SQLi reduit : ORM correct |
| Verifie | Chaque constat valide par test dynamique, SonarQube ou lecture du code |

### Points positifs du projet

- ORM SQLAlchemy utilise partout (pas de SQLi)
- Rate limiting fonctionnel (429 OK)
- Soft delete + audit trail
- Architecture Clean Architecture

### Conclusion

8 constats, 4 critiques, 22 actions de remediation
Priorite immediate : bcrypt + fermer port BDD + RBAC
