-- ===================================================================
-- CREATION DES ROLES ET SECURISATION DES BASES ET SCHEMAS POSTGRESQL
-- ===================================================================

-------------------------
-- 1. Création des rôles
-------------------------
\c postgres

-- Pour la base mspr
CREATE USER etl_user WITH PASSWORD 'ETLmspr2025!';
CREATE USER api_user WITH PASSWORD 'APImspr2025!';
CREATE USER alembic_user WITH PASSWORD 'ALEMBICmspr2025!';

-- Pour la base metabase
CREATE USER metabase_user WITH PASSWORD 'METABASEmspr2025!';

------------------------------------------------
-- 2. Sécurisation de la base mspr (à exécuter après création des utilisateurs)
------------------------------------------------
\c mspr

-- a. Interdire la connexion à tous sauf les rôles explicitement listés
REVOKE CONNECT ON DATABASE mspr FROM PUBLIC;
GRANT CONNECT ON DATABASE mspr TO etl_user, api_user, alembic_user;

-- b. Sécurisation du schéma public
REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO etl_user, api_user, alembic_user;

-- c. Droits sur les tables
GRANT SELECT ON ALL TABLES IN SCHEMA public TO etl_user;
GRANT INSERT, UPDATE ON statistic, daily_wise TO etl_user;

GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO api_user;

GRANT ALL PRIVILEGES ON DATABASE mspr TO alembic_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO alembic_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO alembic_user;

-- Facultatif : Appliquer les droits par défaut sur les futures tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO etl_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT INSERT, UPDATE ON TABLES TO etl_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE ON TABLES TO api_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO alembic_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO alembic_user;

------------------------------------------------
-- 3. Sécurisation de la base metabase (à exécuter après création des utilisateurs)
------------------------------------------------
\c metabase

REVOKE CONNECT ON DATABASE metabase FROM PUBLIC;
GRANT CONNECT ON DATABASE metabase TO metabase_user;

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO metabase_user;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO metabase_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO metabase_user;

------------------------------------------------
-- 4. BONUS : Interdire l'accès à toute nouvelle base par défaut
------------------------------------------------
-- A exécuter dans chaque nouvelle base, ou ajouter dans un script de post-install :
-- REVOKE CONNECT ON DATABASE nouvelle_base FROM PUBLIC;