-- ===================================================================
-- BLOC DE SUPPRESSION EN CASCADE (Downgrade/Clean)
-- ===================================================================
-- A lancer pour "désinstaller" proprement les rôles, transférer la propriété et nettoyer les droits

-------------------------------
-- Nettoyage de la base mspr
-------------------------------
\c mspr

-- Transférer la propriété des objets possédés par les rôles vers postgres (ou un autre superuser)
REASSIGN OWNED BY etl_user, api_user, alembic_user TO postgres;
-- Supprimer tous les droits accordés dans cette base
DROP OWNED BY etl_user, api_user, alembic_user;

-------------------------------
-- Nettoyage de la base metabase
-------------------------------
\c metabase

REASSIGN OWNED BY metabase_user TO postgres;
DROP OWNED BY metabase_user;

-------------------------------
-- Suppression des utilisateurs (à faire hors connexion à une base)
-------------------------------
-- Revenir sur la base postgres (ou toute autre base "neutre")
\c postgres

DROP USER IF EXISTS etl_user;
DROP USER IF EXISTS api_user;
DROP USER IF EXISTS alembic_user;
DROP USER IF EXISTS metabase_user;

-- ===================================================================
-- Fin du script
-- ===================================================================