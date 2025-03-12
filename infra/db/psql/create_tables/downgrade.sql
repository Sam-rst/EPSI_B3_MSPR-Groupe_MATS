-- Supprimer les tables pivot d'abord (évite erreurs de clés étrangères)
DROP TABLE IF EXISTS daily_wise_link_vaccine CASCADE;
DROP TABLE IF EXISTS users_group_role CASCADE;

-- Supprimer les tables principales
DROP TABLE IF EXISTS statistic CASCADE;
DROP TABLE IF EXISTS daily_wise CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS country CASCADE;
DROP TABLE IF EXISTS role CASCADE;
DROP TABLE IF EXISTS gender CASCADE;
DROP TABLE IF EXISTS vaccine CASCADE;
DROP TABLE IF EXISTS epidemic CASCADE;
DROP TABLE IF EXISTS continent CASCADE;

-- Supprimer la fonction de mise à jour automatique des updated_at
DROP FUNCTION IF EXISTS update_timestamp CASCADE;

-- Supprimer les triggers associés
DO $$ 
DECLARE 
   table_name TEXT;
BEGIN 
   FOR table_name IN 
      SELECT tablename 
      FROM pg_tables 
      WHERE schemaname = 'public' AND tablename IN ('continent', 'vaccine', 'gender', 'role', 'country', 'users', 'daily_wise', 'statistic') 
   LOOP
      EXECUTE format('DROP TRIGGER IF EXISTS set_timestamp_%I ON %I;', table_name, table_name);
   END LOOP;
END $$;
