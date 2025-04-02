import pandas as pd
import psycopg2
from psycopg2 import sql
from datetime import datetime

# === CONFIGURATION DE LA BASE DE DONNÉES ===
DB_CONFIG = {
    "host": "localhost",
    "dbname": "mspr",
    "user": "postgres",
    "password": "postgres",
    "port": 2345
}

# === LECTURE DU CSV ===
CSV_FILE = "./cleaned/country_vaccinations_by_manufacturer_cleaned.csv"
df = pd.read_csv(CSV_FILE)

# Connexion à PostgreSQL
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

def get_or_create_country(country_name):
    try:
        cur.execute("SELECT id FROM country WHERE name = %s AND is_deleted IS NOT TRUE", (country_name,))
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            print(f"[INFO] Insertion du pays manquant : '{country_name}'")
            cur.execute("""
                INSERT INTO country (name, iso2, iso3, population, continent_id, is_deleted)
                VALUES (%s, NULL, NULL, NULL, NULL, FALSE)
                RETURNING id
            """, (country_name,))
            return cur.fetchone()[0]
    except Exception as e:
        print(f"[ERROR] Erreur lors de l'insertion du pays '{country_name}' : {e}")
        conn.rollback()
        return None

def get_or_create_vaccine(vaccine_name):
    cur.execute("SELECT id FROM vaccine WHERE name = %s AND is_deleted IS NOT TRUE", (vaccine_name,))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        # Insertion minimale avec valeurs par défaut (modifie selon besoin)
        cur.execute("""
            INSERT INTO vaccine (name, laboratory, epidemic_id, id, is_deleted)
            VALUES (%s, %s, 1, DEFAULT, FALSE)
            RETURNING id
        """, (vaccine_name, 'Unknown'))
        return cur.fetchone()[0]

def insert_daily_wise(date, country_id):
    cur.execute("""
        INSERT INTO daily_wise (date, country_id, id, is_deleted)
        VALUES (%s, %s, DEFAULT, FALSE)
        RETURNING id
    """, (date, country_id))
    return cur.fetchone()[0]

def insert_statistic(label, value, country_id, epidemic_id, daily_wise_id):
    cur.execute("""
        INSERT INTO statistic (
            label, value, country_id, epidemic_id, dayly_wise_id, id, is_deleted
        ) VALUES (%s, %s, %s, %s, %s, DEFAULT, FALSE)
    """, (label, value, country_id, epidemic_id, daily_wise_id))

# === INSERTION DES DONNÉES ===
for _, row in df.iterrows():
    # conn.rollback()
    country = row['Country']
    vaccine = row['Vaccine']
    report_date = row['ReportDate']
    total_vaccinations = row['TotalVaccination']

    try:
        # Conversion date
        report_date = datetime.strptime(report_date, "%Y-%m-%d")

        country_id = get_or_create_country(country)
        if not country_id:
            continue

        vaccine_id = get_or_create_vaccine(vaccine)

        daily_wise_id = insert_daily_wise(report_date, country_id)

        # Insertion de la statistique
        insert_statistic(
            label="totalVaccination",
            value=float(total_vaccinations),
            country_id=country_id,
            epidemic_id=1,  
            daily_wise_id=daily_wise_id
        )

        conn.commit()

        print(f"[OK] {country} - {report_date} - {vaccine} - {total_vaccinations}")

    except Exception as e:
        print(f"[ERROR] Ligne ignorée : {e}")
        print("→ Ligne concernée :", row)
        conn.rollback()

# Validation et fermeture
conn.commit()
cur.close()
conn.close()
print("✅ Import terminé.")
