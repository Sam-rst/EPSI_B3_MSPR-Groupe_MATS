import psycopg2
from psycopg2 import sql
import pandas as pd
import os
import yaml
from datetime import datetime
from tqdm import tqdm


class PostgresConnector:
    def __init__(
        self,
        host="localhost",
        database="mspr",
        port=5432,
    ):
        """
        Initialise la connexion a PostgreSQL.
        Les credentials sont obligatoirement fournis par variables d'environnement (fix C5).
        """
        self.connection_params = {
            "host": os.environ.get("ETL_POSTGRES_HOST", host),
            "database": os.environ.get("ETL_POSTGRES_DB", database),
            "user": os.environ["ETL_POSTGRES_USER"],
            "password": os.environ["ETL_POSTGRES_PASSWORD"],
            "port": int(os.environ.get("ETL_POSTGRES_PORT", port)),
        }
        self.connection = None
        self.cursor = None

    def connect(self):
        """Établit une connexion à la base de données PostgreSQL"""
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            self.cursor = self.connection.cursor()
            print(
                f"Connexion établie à {self.connection_params['database']} sur {self.connection_params['host']}"
            )
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

    def execute_etl_process(
        self,
        mappings_path=None,  # on laisse None par défaut
        base_folder="../cleaned",
        specific_files=None,  # nouveau paramètre
    ):
        """
        Exécute le processus ETL pour charger les données dans PostgreSQL.

        Args:
            mappings_path (str, optional): Chemin vers le fichier de mappings.
                Par défaut, recherche un fichier mappings.yaml dans le même dossier.
            base_folder (str, optional): Dossier contenant les fichiers CSV nettoyés.
                Par défaut "../cleaned".
            specific_files (str or list, optional): Nom du fichier ou liste des noms de fichiers à traiter.
                Si None, tous les fichiers définis dans le mapping sont traités.
        """
        if mappings_path is None:
            # On calcule un chemin absolu vers mappings.yaml
            current_dir = os.path.dirname(__file__)  # dossier contenant load.py
            mappings_path = os.path.join(current_dir, "mappings.yaml")

        with open(mappings_path, "r", encoding="utf-8") as f:
            mappings = yaml.safe_load(f)

        # Convertir specific_files en liste si c'est une chaîne
        if specific_files and isinstance(specific_files, str):
            specific_files = [specific_files]

        print("✅ Mappings chargés :", mappings)
        print("🧪 Nombre de fichiers à traiter :", len(mappings.get("files", [])))
        print("🧬 Type de chaque entrée :")
        for i, f in enumerate(mappings.get("files", [])):
            print(f"   - [{i}] {f} (type={type(f)})")

        def find_continent_id(cur, continent_name):
            """Recherche l'ID d'un continent par son nom, retourne 1 si non trouvé"""
            if not continent_name:
                return 1

            cur.execute(
                "SELECT id FROM continent WHERE name LIKE %s AND is_deleted IS NOT TRUE",
                (f"%{continent_name}%",),
            )
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                print(
                    f"⚠️ Continent '{continent_name}' non trouvé, utilisation de l'ID par défaut (1)"
                )
                return 1

        def find_country_id(cur, country_name):
            """Recherche l'ID d'un pays par son nom, retourne 1 si non trouvé"""
            if not country_name:
                return 1

            cur.execute(
                "SELECT id FROM country WHERE name LIKE %s AND is_deleted IS NOT TRUE",
                (f"%{country_name}%",),
            )
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                print(
                    f"⚠️ Pays '{country_name}' non trouvé, utilisation de l'ID par défaut (1)"
                )
                return 1

        def find_vaccine_id(cur, vaccine_name):
            """Recherche l'ID d'un vaccin par son nom, retourne 1 si non trouvé"""
            if not vaccine_name:
                return 1

            cur.execute(
                "SELECT id FROM vaccine WHERE name LIKE %s AND is_deleted IS NOT TRUE",
                (f"%{vaccine_name}%",),
            )
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                print(
                    f"⚠️ Vaccin '{vaccine_name}' non trouvé, utilisation de l'ID par défaut (1)"
                )
                return 1

        def find_epidemic_id(cur, epidemic_name="COVID-19"):
            """Recherche l'ID d'une épidémie par son nom, retourne 1 si non trouvé"""
            cur.execute(
                "SELECT id FROM epidemic WHERE name LIKE %s AND is_deleted IS NOT TRUE",
                (f"%{epidemic_name}%",),
            )
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                print(
                    f"⚠️ Épidémie '{epidemic_name}' non trouvée, utilisation de l'ID par défaut (1)"
                )
                return 1

        def insert_daily_wise(
            cur, report_date, country_id, province=None, lat=None, lon=None
        ):
            """Insère une entrée dans daily_wise"""
            cur.execute(
                """
                INSERT INTO daily_wise (date, province, latitude, longitude, country_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """,
                (report_date, province, lat, lon, country_id),
            )
            return cur.fetchone()[0]

        def insert_statistic(
            cur, label, value, country_id, epidemic_id, daily_wise_id, vaccine_id
        ):
            """Insère une statistique"""
            if pd.isna(value):
                return

            cur.execute(
                """
                INSERT INTO statistic (
                    label, value, country_id, epidemic_id, daily_wise_id, vaccine_id
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """,
                (
                    label,
                    float(value),
                    country_id,
                    epidemic_id,
                    daily_wise_id,
                    vaccine_id,
                ),
            )

        def process_file(conn, cur, file_path, config):
            """Traite un fichier CSV en recherchant les ID existants ou en utilisant l'ID par défaut"""
            df = pd.read_csv(file_path)
            df.columns = [col.strip() for col in df.columns]
            mapping = config["mapping"]
            report_date_col = mapping.get("report_date", "today")

            # ID par défaut pour l'épidémie (COVID-19)
            epidemic_id = find_epidemic_id(cur)

            for _, row in tqdm(df.iterrows(), total=len(df), desc=file_path):
                try:
                    # Rechercher l'ID du continent si spécifié
                    continent_id = 1  # ID par défaut
                    if "continent" in mapping:
                        continent_col = mapping.get("continent")
                        continent = (
                            row[continent_col]
                            if continent_col and continent_col in row
                            else None
                        )
                        if continent:
                            continent_id = find_continent_id(cur, continent)

                    # Rechercher l'ID du pays
                    country_id = 1  # ID par défaut
                    country_col = mapping.get("country")
                    if country_col and country_col in row:
                        country = row[country_col]
                        if country and country != "World":
                            country_id = find_country_id(cur, country)

                    # Rechercher l'ID du vaccin si spécifié
                    vaccine_id = 1  # ID par défaut
                    if "vaccine" in mapping:
                        vaccine_col = mapping["vaccine"]
                        vaccine_name = (
                            row[vaccine_col]
                            if vaccine_col and vaccine_col in row
                            else None
                        )
                        if vaccine_name:
                            vaccine_id = find_vaccine_id(cur, vaccine_name)

                    # Détermination de la date
                    report_date = (
                        datetime.today()
                        if report_date_col == "today"
                        else datetime.strptime(
                            str(row.get(report_date_col)), "%Y-%m-%d"
                        )
                    )

                    # Récupérer province et coordonnées si présents
                    province_col = mapping.get("province")
                    province = (
                        row[province_col]
                        if province_col and province_col in row
                        else None
                    )
                    lat_col = mapping.get("latitude")
                    lat = row[lat_col] if lat_col and lat_col in row else None
                    lon_col = mapping.get("longitude")
                    lon = row[lon_col] if lon_col and lon_col in row else None

                    # Insérer une entrée daily_wise
                    daily_wise_id = insert_daily_wise(
                        cur, report_date, country_id, province, lat, lon
                    )

                    # Insérer les statistiques
                    for stat in mapping.get("statistics", []):
                        label = stat["label"]
                        column = stat["column"]
                        if column in row:
                            value = row[column]
                            insert_statistic(
                                cur,
                                label,
                                value,
                                country_id,
                                epidemic_id,
                                daily_wise_id,
                                vaccine_id,
                            )
                        else:
                            print(
                                f"⚠️ Colonne '{column}' non trouvée dans le CSV pour la statistique '{label}'"
                            )

                    conn.commit()
                except Exception as e:
                    import traceback

                    traceback.print_exc()
                    print(f"[ERROR] Ligne ignorée : {e}")
                    conn.rollback()

        # Vérification de la connexion à la base de données
        if not self.connection or self.connection.closed:
            if not self.connect():
                return False

        # Filtrer les entrées si specific_files est spécifié
        if specific_files:
            files_to_process = [
                entry for entry in mappings["files"] if entry["name"] in specific_files
            ]
            if not files_to_process:
                print(
                    f"⚠️ Aucun fichier spécifié trouvé dans les mappings : {specific_files}"
                )
                return False
        else:
            files_to_process = mappings["files"]

        # Afficher le nombre de fichiers qui seront traités
        print(f"📝 Nombre de fichiers qui seront traités : {len(files_to_process)}")

        # Traiter chaque fichier
        for entry in files_to_process:
            try:
                print(f'\n➡️ Traitement du fichier : {entry["name"]}')
                file_path = os.path.join(base_folder, entry["name"])

                if os.path.exists(file_path):
                    process_file(self.connection, self.cursor, file_path, entry)
                    print(f"✅ Fichier traité avec succès : {entry['name']}")
                else:
                    print(f"⚠️ Fichier non trouvé : {file_path}")
            except Exception as e:
                import traceback

                print(f"💥 Erreur lors du traitement de l'entrée : {entry['name']}")
                traceback.print_exc()

        print("\n✅ Traitement ETL terminé")
        return True
