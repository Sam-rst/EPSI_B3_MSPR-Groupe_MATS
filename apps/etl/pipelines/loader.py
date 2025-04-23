import pandas as pd
import psycopg2
import yaml
from datetime import datetime
from tqdm import tqdm
import os

# === CONFIGURATION DE LA BASE DE DONNÉES ===
DB_CONFIG = {
    "host": "?",
    "dbname": "?",
    "user": "?",
    "password": "?",
    "port": "?",
}

# === UTILITAIRES BASE ===
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

# === TRAITEMENT ===
def process_file(cur, file_path, config):
    print(f"\n📦 === Traitement de : {os.path.basename(file_path)} ===")
    df = pd.read_csv(file_path)
    df.columns = [col.strip() for col in df.columns]

    mapping = config['mapping']
    report_date_col = mapping.get('report_date', 'today')

    for _, row in tqdm(df.iterrows(), total=len(df), desc=os.path.basename(file_path)):
        try:
            continent_id = None
            if 'continent' in mapping:
                continent = row.get(mapping['continent'])
                continent_id = get_or_create_continent(cur, continent)

            country_name = mapping.get('country', 'World')
            country = row.get(country_name) if country_name != 'World' else 'World'
            country_id = get_or_create_country(cur, country, continent_id)

            if 'population' in mapping:
                population = row.get(mapping['population'])
                if population:
                    try:
                        cur.execute("UPDATE country SET population = %s WHERE id = %s", (int(population), country_id))
                    except:
                        pass

            # Détermination de la date
            if report_date_col == 'today':
                report_date = datetime.today()
            else:
                report_date = datetime.strptime(row.get(report_date_col), "%Y-%m-%d")

            # Province et coordonnées si présentes
            province = row.get(mapping.get('province')) if 'province' in mapping else None
            lat = row.get(mapping.get('latitude')) if 'latitude' in mapping else None
            lon = row.get(mapping.get('longitude')) if 'longitude' in mapping else None

            daily_wise_id = insert_daily_wise(cur, report_date, country_id, province, lat, lon)

            for stat in mapping.get('statistics', []):
                label = stat['label']
                value = row.get(stat['column'])
                insert_statistic(cur, label, value, country_id, 1, daily_wise_id)

            conn.commit()
            print(f"[OK] [{os.path.basename(file_path)}] {country} - {report_date}")

        except Exception as e:
            print(f"[ERROR] Ligne ignorée : {e}")
            print("→ Ligne concernée :", row)
            conn.rollback()

# === MAIN ===
if __name__ == "__main__":
    with open("mappings.yaml", "r", encoding="utf-8") as f:
        mappings = yaml.safe_load(f)

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    for entry in mappings['files']:
        file_name = entry['name']
        file_path = os.path.join("../cleaned", file_name)

        if os.path.exists(file_path):
            process_file(cur, file_path, entry)
        else:
            print(f"⚠️  Fichier non trouvé : {file_path}")

    cur.close()
    conn.close()
    print("\n✅ Tous les fichiers ont été traités.")
