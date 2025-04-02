import psycopg2
from psycopg2 import sql
import pandas as pd
import os

class PostgresConnector:
    def __init__(self, host="localhost", database="mspr", user="postgres", password="postgres", port=5432):
        """
        Initialise la connexion à PostgreSQL avec les valeurs par défaut
        fournies ou des valeurs d'environnement si disponibles
        """
        self.connection_params = {
            'host': os.environ.get('POSTGRES_HOST', host),
            'database': os.environ.get('POSTGRES_DB', database),
            'user': os.environ.get('POSTGRES_USER', user),
            'password': os.environ.get('POSTGRES_PASSWORD', password),
            'port': int(os.environ.get('POSTGRES_PORT', port))
        }
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Établit une connexion à la base de données PostgreSQL"""
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            self.cursor = self.connection.cursor()
            print(f"Connexion établie à {self.connection_params['database']} sur {self.connection_params['host']}")
            return True
        except Exception as e:
            print(f"Erreur de connexion à PostgreSQL: {e}")
            return False
    
    def disconnect(self):
        """Ferme la connexion à la base de données"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Connexion à PostgreSQL fermée")
    
    def execute_query(self, query, params=None):
        """Exécute une requête SQL"""
        if not self.connection or self.connection.closed:
            if not self.connect():
                return None
        
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            print("Requête exécutée avec succès")
            return True
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête: {e}")
            self.connection.rollback()
            return False
    
    def execute_script(self, script):
        """Exécute un script SQL complet avec plusieurs requêtes"""
        if not self.connection or self.connection.closed:
            if not self.connect():
                return None
        
        try:
            self.cursor.execute(script)
            self.connection.commit()
            print("Script SQL exécuté avec succès")
            return True
        except Exception as e:
            print(f"Erreur lors de l'exécution du script SQL: {e}")
            self.connection.rollback()
            return False
    
    def load_csv_to_staging(self, csv_path, table_name='staging_country_vaccinations'):
        """Charge un fichier CSV dans une table de staging"""
        if not self.connection or self.connection.closed:
            if not self.connect():
                return False
                
        try:
            # Vérifier si la table existe, sinon la créer
            check_table_query = f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = '{table_name}'
            );
            """
            self.cursor.execute(check_table_query)
            table_exists = self.cursor.fetchone()[0]
            
            if not table_exists:
                create_table_query = f"""
                CREATE TABLE {table_name} (
                    country TEXT,
                    vaccine TEXT,
                    report_date DATE,
                    total_vaccination BIGINT,
                    file_loaded_at TIMESTAMP DEFAULT NOW()
                );
                """
                self.cursor.execute(create_table_query)
                self.connection.commit()
            
            # Utiliser COPY pour charger le CSV
            with open(csv_path, 'r') as f:
                next(f)  # Sauter l'en-tête
                self.cursor.copy_expert(
                    f"COPY {table_name} (country, vaccine, report_date, total_vaccination) FROM STDIN WITH CSV",
                    f
                )
            
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Erreur lors du chargement du CSV: {e}")
            self.connection.rollback()
            return False
            
    def execute_etl_process(self, csv_path):
        """Exécute le processus ETL complet basé sur le script SQL fourni"""
        # Étape 1: Charger le CSV dans la table de staging
        if not self.load_csv_to_staging(csv_path):
            return False
            
        # Étape 2: Exécuter le script ETL
        etl_script = """
        -- 3) Insérer dans country
        INSERT INTO country (name, created_by)
        SELECT DISTINCT s.country, 'ETL_script'
        FROM staging_country_vaccinations s
        WHERE s.country IS NOT NULL
          AND s.country <> ''
          AND NOT EXISTS (
              SELECT 1 FROM country c WHERE c.name = s.country
          );

        -- 4) Insérer dans vaccine
        INSERT INTO vaccine (name, created_by)
        SELECT DISTINCT s.vaccine, 'ETL_script'
        FROM staging_country_vaccinations s
        WHERE s.vaccine IS NOT NULL
          AND s.vaccine <> ''
          AND NOT EXISTS (
              SELECT 1 FROM vaccine v WHERE v.name = s.vaccine
          );

        -- 5) Insérer dans daily_wise
        INSERT INTO daily_wise (date, province_name, latitude, longitude, created_by, country_id)
        SELECT s.report_date, NULL, NULL, NULL, 'ETL_script', c.id
        FROM staging_country_vaccinations s
        JOIN country c ON c.name = s.country
        WHERE s.report_date IS NOT NULL
          AND NOT EXISTS (
              SELECT 1 FROM daily_wise dw
              WHERE dw.date = s.report_date
                AND dw.country_id = c.id
          );

        -- 6) Insérer la statistique "TotalVaccination"
        INSERT INTO statistic (label, value, created_by, country_id, dw_id)
        SELECT 'TotalVaccination',
               s.total_vaccination,
               'ETL_script',
               c.id,
               dw.id
        FROM staging_country_vaccinations s
        JOIN country c ON c.name = s.country
        JOIN daily_wise dw ON dw.date = s.report_date
                           AND dw.country_id = c.id
        WHERE s.total_vaccination IS NOT NULL
          AND s.total_vaccination > 0
          AND NOT EXISTS (
              SELECT 1 FROM statistic st
              WHERE st.label = 'TotalVaccination'
                AND st.country_id = c.id
                AND st.dw_id = dw.id
          );

        -- 7) Lier daily_wise et vaccine (table pivot)
        INSERT INTO daily_wise_link_vaccine (dw_id, vaccine_id)
        SELECT dw.id, v.id
        FROM staging_country_vaccinations s
        JOIN country c ON c.name = s.country
        JOIN daily_wise dw ON dw.date = s.report_date
                           AND dw.country_id = c.id
        JOIN vaccine v ON v.name = s.vaccine
        GROUP BY dw.id, v.id;
        """
        
        return self.execute_script(etl_script)