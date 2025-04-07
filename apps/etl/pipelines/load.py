import psycopg2
from psycopg2 import sql
import pandas as pd
import os
import yaml
from datetime import datetime
from tqdm import tqdm

class PostgresConnector:
    def __init__(self, host="localhost", database="mspr", user="postgres", password="postgres", port=2345):
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
            import traceback
            traceback.print_exc()
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
            import traceback
            traceback.print_exc()
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
            import traceback
            traceback.print_exc()
            print(f"Erreur lors de l'exécution du script SQL: {e}")
            self.connection.rollback()
            return False
    
    # def load_csv_to_staging(self, csv_path, table_name='staging_country_vaccinations'):
    #     """Charge un fichier CSV dans une table de staging"""
    #     if not self.connection or self.connection.closed:
    #         if not self.connect():
    #             return False
                
    #     try:
    #         # Vérifier si la table existe, sinon la créer
    #         check_table_query = f"""
    #         SELECT EXISTS (
    #             SELECT FROM information_schema.tables 
    #             WHERE table_name = '{table_name}'
    #         );
    #         """
    #         self.cursor.execute(check_table_query)
    #         table_exists = self.cursor.fetchone()[0]
            
    #         if not table_exists:
    #             create_table_query = f"""
    #             CREATE TABLE {table_name} (
    #                 country TEXT,
    #                 vaccine TEXT,
    #                 report_date DATE,
    #                 total_vaccination BIGINT,
    #                 file_loaded_at TIMESTAMP DEFAULT NOW()
    #             );
    #             """
    #             self.cursor.execute(create_table_query)
    #             self.connection.commit()
            
    #         # Utiliser COPY pour charger le CSV
    #         with open(csv_path, 'r') as f:
    #             next(f)  # Sauter l'en-tête
    #             self.cursor.copy_expert(
    #                 f"COPY {table_name} (country, vaccine, report_date, total_vaccination) FROM STDIN WITH CSV",
    #                 f
    #             )
            
    #         self.connection.commit()
    #         return True
    #     except Exception as e:
    #         import traceback
    #         traceback.print_exc()
    #         print(f"Erreur lors du chargement du CSV: {e}")
    #         self.connection.rollback()
    #         return False
            
    
    def execute_etl_process(
        self,
        mappings_path=None,                                                         # on laisse None par défaut
        base_folder="../cleaned"
    ):
        if mappings_path is None:
            # On calcule un chemin absolu vers mappings.yaml
            current_dir = os.path.dirname(__file__)                                 # dossier contenant load.py
            mappings_path = os.path.join(current_dir, "mappings.yaml")

        with open(mappings_path, "r", encoding="utf-8") as f:
            mappings = yaml.safe_load(f)
        def get_or_create_continent(cur, continent_name):
            if not continent_name:
                return None
            cur.execute("SELECT id FROM continent WHERE name = %s AND is_deleted IS NOT TRUE", (continent_name,))
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                cur.execute("""
                    INSERT INTO continent (name, code, population, id, is_deleted)
                    VALUES (%s, %s, %s, DEFAULT, FALSE)
                    RETURNING id
                """, (continent_name, 'N/A', 0))
                return cur.fetchone()[0]

        def get_or_create_country(cur, country_name, continent_id=None):
            cur.execute("SELECT id FROM country WHERE name = %s AND is_deleted IS NOT TRUE", (country_name,))
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                cur.execute("""
                    INSERT INTO country (name, iso2, iso3, population, continent_id, id, is_deleted)
                    VALUES (%s, NULL, NULL, NULL, %s, DEFAULT, FALSE)
                    RETURNING id
                """, (country_name, continent_id))
                return cur.fetchone()[0]

        def insert_daily_wise(cur, report_date, country_id, province=None, lat=None, lon=None):
            cur.execute("""
                INSERT INTO daily_wise (date, province, latitude, longitude, country_id, id, is_deleted)
                VALUES (%s, %s, %s, %s, %s, DEFAULT, FALSE)
                RETURNING id
            """, (report_date, province, lat, lon, country_id))
            return cur.fetchone()[0]

        def insert_statistic(cur, label, value, country_id, epidemic_id, daily_wise_id):
            if pd.isna(value):
                return
            cur.execute("""
                INSERT INTO statistic (
                    label, value, country_id, epidemic_id, dayly_wise_id, id, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, DEFAULT, FALSE)
            """, (label, float(value), country_id, epidemic_id, daily_wise_id))
        
        def get_or_create_vaccine(cur, vaccine_name):
            if not vaccine_name:
                return None
            cur.execute("SELECT id FROM vaccine WHERE name = %s AND is_deleted IS NOT TRUE", (vaccine_name,))
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                cur.execute("""
                    INSERT INTO vaccine (name, id, is_deleted)
                    VALUES (%s, DEFAULT, FALSE)
                    RETURNING id
                """, (vaccine_name,))
                return cur.fetchone()[0]

        def process_file(conn, cur, file_path, config):
            df = pd.read_csv(file_path)
            df.columns = [col.strip() for col in df.columns]
            mapping = config['mapping']
            report_date_col = mapping.get('report_date', 'today')

            for _, row in tqdm(df.iterrows(), total=len(df), desc=file_path):
                try:
                    continent_id = None
                    if 'continent' in mapping:
                        continent_col = mapping.get('continent')
                        continent = row[continent_col] if continent_col and continent_col in row else None
                        continent_id = get_or_create_continent(cur, continent)

                    country_col = mapping.get('country')
                    country = row[country_col] if country_col in row else 'World'
                    country_id = get_or_create_country(cur, country, continent_id)

                    if 'population' in mapping:
                        population_col = mapping.get('population')
                        population = row[population_col] if population_col and population_col in row else None
                        if population:
                            try:
                                cur.execute("UPDATE country SET population = %s WHERE id = %s", (int(population), country_id))
                            except:
                                pass
                    
                    # Ajout vaccine
                    if 'vaccine' in mapping:
                        vaccine_col = mapping['vaccine']
                        vaccine_name = row[vaccine_col] if vaccine_col and vaccine_col in row else None
                        if vaccine_name:
                            get_or_create_vaccine(cur, vaccine_name)        

                    report_date = datetime.today() if report_date_col == 'today' else datetime.strptime(row.get(report_date_col), "%Y-%m-%d")

                    province_col = mapping.get('province')
                    province = row[province_col] if province_col and province_col in row else None
                    lat_col = mapping.get('latitude')
                    lat = row[lat_col] if lat_col and lat_col in row else None
                    lon_col = mapping.get('longitude')
                    lon = row[lon_col] if lon_col and lon_col in row else None

                    daily_wise_id = insert_daily_wise(cur, report_date, country_id, province, lat, lon)

                    for stat in mapping.get('statistics', []):
                            label = stat['label']
                            column = stat['column']
                            value = row[column] if column in row else None
                            insert_statistic(cur, label, value, country_id, 1, daily_wise_id)

                    conn.commit()
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    print(f"[ERROR] Ligne ignorée : {e}")
                    conn.rollback()

        import os
        with open(mappings_path, "r", encoding="utf-8") as f:
            mappings = yaml.safe_load(f)

        print("✅ Mappings chargés :", mappings)
        print("🧪 Nombre de fichiers à traiter :", len(mappings.get('files', [])))
        print("🧬 Type de chaque entrée :")
        for i, f in enumerate(mappings.get('files', [])):
            print(f"   - [{i}] {f} (type={type(f)})")


        if not self.connection or self.connection.closed:
            if not self.connect():
                return False

        for entry in mappings['files']:
            try:
                print('➡️ Entry en cours :', entry)
                file_name = entry['name']
                file_path = os.path.join(base_folder, file_name)

                if os.path.exists(file_path):
                    process_file(self.connection, self.cursor, file_path, entry)
                else:
                    print(f"⚠️  Fichier non trouvé : {file_path}")
                    print(f"⚠️  Fichier non trouvé : {file_path}")
            except Exception as e:
                import traceback
                print(f"💥 Erreur lors du traitement de l'entrée : {entry}")
                traceback.print_exc()
