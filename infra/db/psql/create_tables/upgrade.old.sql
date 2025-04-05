-- Table Continent
CREATE TABLE continent (
   id SERIAL PRIMARY KEY,
   name VARCHAR(50) NOT NULL,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   created_by VARCHAR(50),
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_by VARCHAR(50)
);

-- Table Gender
CREATE TABLE gender (
   id SERIAL PRIMARY KEY,
   name VARCHAR(50) NOT NULL,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   created_by VARCHAR(50),
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_by VARCHAR(50)
);

-- Table Role
CREATE TABLE role (
   id SERIAL PRIMARY KEY,
   name VARCHAR(50) NOT NULL,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   created_by VARCHAR(50),
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_by VARCHAR(50)
);

-- Table Epidemic
CREATE TABLE epidemic (
   id SERIAL PRIMARY KEY,
   name VARCHAR(50) NOT NULL,
   type VARCHAR(50) NOT NULL,
   description TEXT,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   created_by VARCHAR(50),
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_by VARCHAR(50)
);

-- Table Vaccine
CREATE TABLE vaccine (
   id SERIAL PRIMARY KEY,
   name VARCHAR(50) NOT NULL,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   created_by VARCHAR(50),
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_by VARCHAR(50),
   epidemic_id INT REFERENCES epidemic(id) ON DELETE SET NULL
);

-- Table Country
CREATE TABLE country (
   id SERIAL PRIMARY KEY,
   name VARCHAR(50) NOT NULL,
   iso2 CHAR(2),
   iso3 CHAR(3),
   code3 VARCHAR(50),
   population INT,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   created_by VARCHAR(50),
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_by VARCHAR(50),
   continent_id INT REFERENCES continent(id) ON DELETE SET NULL
);

-- Table Users
CREATE TABLE users (
   id SERIAL PRIMARY KEY,
   email VARCHAR(360) NOT NULL UNIQUE,
   firstname VARCHAR(255),
   lastname VARCHAR(255),
   username VARCHAR(50) UNIQUE,
   password TEXT NOT NULL,
   last_connection TIMESTAMP,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   created_by VARCHAR(50),
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_by VARCHAR(50),
   gender_id INT REFERENCES gender(id) ON DELETE SET NULL
);

-- Table DailyWise
CREATE TABLE daily_wise (
   id SERIAL PRIMARY KEY,
   date DATE NOT NULL,
   province_name VARCHAR(50),
   latitude DECIMAL(9,6),
   longitude DECIMAL(9,6),
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   created_by VARCHAR(50),
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_by VARCHAR(50),
   country_id INT REFERENCES country(id) ON DELETE SET NULL
);

-- Table Statistic
CREATE TABLE statistic (
   id SERIAL PRIMARY KEY,
   label VARCHAR(50) NOT NULL,
   value DOUBLE PRECISION NOT NULL,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   created_by VARCHAR(50),
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_by VARCHAR(50),
   published_at TIMESTAMP,
   published_by VARCHAR(50),
   country_id INT REFERENCES country(id) ON DELETE SET NULL,
   dw_id INT REFERENCES daily_wise(id) ON DELETE SET NULL,
   epidemic_id INT REFERENCES epidemic(id) ON DELETE SET NULL
);

-- Table pivot DailyWise <-> Vaccine
CREATE TABLE daily_wise_link_vaccine (
   dw_id INT REFERENCES daily_wise(id) ON DELETE CASCADE,
   vaccine_id INT REFERENCES vaccine(id) ON DELETE CASCADE,
   PRIMARY KEY(dw_id, vaccine_id)
);

-- Table pivot Users <-> Role
CREATE TABLE users_group_role (
   user_id INT REFERENCES users(id) ON DELETE CASCADE,
   role_id INT REFERENCES role(id) ON DELETE CASCADE,
   PRIMARY KEY(user_id, role_id)
);

-- Trigger pour mettre à jour automatiquement updated_at sur modification
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Ajout du trigger à toutes les tables contenant updated_at
DO $$ 
DECLARE 
   table_name TEXT;
BEGIN 
   FOR table_name IN 
      SELECT tablename 
      FROM pg_tables 
      WHERE schemaname = 'public' AND tablename IN ('continent', 'vaccine', 'epidemic', 'gender', 'role', 'country', 'users', 'daily_wise', 'statistic') 
   LOOP
      EXECUTE format('
         CREATE TRIGGER set_timestamp_%I
         BEFORE UPDATE ON %I
         FOR EACH ROW
         EXECUTE FUNCTION update_timestamp();
      ', table_name, table_name);
   END LOOP;
END $$;
