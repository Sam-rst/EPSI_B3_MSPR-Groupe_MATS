-------------------------------------------------
-------------------------------------------------
         REQUETES DE CREATION DE RÖLES
-------------------------------------------------
-------------------------------------------------

CREATE USER etl_user WITH PASSWORD '<etl_password>';
GRANT CONNECT ON DATABASE mspr TO etl_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO etl_user;
GRANT INSERT, UPDATE ON statistic, daily_wise TO etl_user;

CREATE USER api_user WITH PASSWORD '<api_password>';
GRANT CONNECT ON DATABASE mspr TO api_user;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO api_user;

CREATE USER alembic_user WITH PASSWORD '<alembic_password>';
GRANT ALL PRIVILEGES ON DATABASE mspr TO alembic_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO alembic_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO alembic_user;

CREATE USER metabase_user WITH PASSWORD '<metabase_password>';
GRANT CONNECT ON DATABASE metabase TO metabase_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO metabase_user;