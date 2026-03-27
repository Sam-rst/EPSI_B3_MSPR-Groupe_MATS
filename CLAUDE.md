# CLAUDE.md - AnalyzeIT (EPSI B3 MSPR - Groupe MATS)

## Projet

Plateforme d'analyse de donnees epidemiologiques combinant ETL, API REST, frontend web et ML.
- **Backend** : FastAPI (Python 3.10), SQLAlchemy, PostgreSQL, JWT (HS256), slowapi (rate limiting)
- **Frontend** : Next.js 15.3.2, React 19, Tailwind CSS 4, Plotly.js
- **ETL** : Python Tkinter GUI, Pandas, psycopg2
- **Infra** : Docker Compose (PostgreSQL, API, Frontend, Metabase, Seeder)
- **CI/CD** : CircleCI (lint, tests, deploy SSH vers VPS)

## Architecture

```
project/
├── apps/
│   ├── api/          # FastAPI - Clean Architecture (presentation/application/domain/infrastructure)
│   ├── etl/          # Application desktop ETL (Tkinter)
│   ├── frontend/     # Next.js web app (port 3030)
│   └── seeder/       # Script d'initialisation des donnees
├── config/env/       # Fichiers de configuration par environnement
├── data/             # Donnees de seed (JSON)
├── docs/             # Documentation (architecture, diagrammes, UML)
├── infra/            # Fichiers infrastructure
└── .circleci/        # Pipeline CI/CD
```

## Gitflow

- **main** : Production (merge uniquement depuis release/hotfix via PR)
- **test** : Environnement de test (merge depuis develop via PR)
- **develop** : Branche d'integration principale
- **feature/MSPR-{code}_{description}** : Nouvelles fonctionnalites
- **bugfix/MSPR-{code}_{description}** : Corrections de bugs
- **hotfix/MSPR-{code}_{description}** : Corrections critiques en production
- **release/MSPR-{tag}** : Preparation de release

> Toujours creer les branches depuis `develop`. Jamais de push direct sur `main` ou `test`.

## Commandes utiles

```bash
# Demarrer l'infrastructure
docker-compose up --build -d

# Acces services
# API:       http://localhost:8000 (docs: /docs)
# Frontend:  http://localhost:3030
# Metabase:  http://localhost:3000
# PostgreSQL: localhost:5432

# Lancer les tests API
cd apps/api && python -m pytest

# Linter
cd apps/api && pylint src/

# Migrations Alembic
cd apps/api && alembic upgrade head
```

## Conventions

- Clean Architecture pour l'API (routers -> usecases -> repositories)
- Soft delete sur toutes les entites (is_deleted, deleted_at, deleted_by)
- Audit trail sur toutes les entites (created_at/by, updated_at/by)
- Dependency Injection via dependency-injector
- Tous les endpoints data necessitent un JWT Bearer token
- Rate limiting configure par endpoint
