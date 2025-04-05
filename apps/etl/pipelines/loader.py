import pandas as pd
import psycopg2
from datetime import datetime
import sys

# === CONFIGURATION DE LA BASE DE DONNÉES ===
DB_CONFIG = {
    "host": "localhost",
    "dbname": "mspr",
    "user": "postgres",
    "password": "postgres",
    "port": 2345
}

# FICHIER À TRAITER
if len(sys.argv) < 2:
    print("❌ Usage: python loader.py [csv_name]")
    sys.exit(1)

CSV_FILE = sys.argv[1]
df = pd.read_csv(CSV_FILE)

# Connexion à PostgreSQL
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

def get_or_create_continent(continent_name):
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

def get_or_create_country(country_name, continent_id=None):
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

def get_or_create_vaccine(vaccine_name):
    cur.execute("SELECT id FROM vaccine WHERE name = %s AND is_deleted IS NOT TRUE", (vaccine_name,))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
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
    if pd.isna(value):
        return
    cur.execute("""
        INSERT INTO statistic (
            label, value, country_id, epidemic_id, dayly_wise_id, id, is_deleted
        ) VALUES (%s, %s, %s, %s, %s, DEFAULT, FALSE)
    """, (label, float(value), country_id, epidemic_id, daily_wise_id))

# === TRAITEMENT ===
if "manufacturer" in CSV_FILE:
    print("📦 Traitement du fichier de vaccins")
    for _, row in df.iterrows():
        country = row['Country']
        vaccine = row['Vaccine']
        report_date = datetime.strptime(row['ReportDate'], "%Y-%m-%d")
        total_vaccinations = row['TotalVaccination']

        try:
            country_id = get_or_create_country(country)
            if not country_id:
                continue

            vaccine_id = get_or_create_vaccine(vaccine)
            daily_wise_id = insert_daily_wise(report_date, country_id)

            insert_statistic(
                label="totalVaccination",
                value=float(total_vaccinations),
                country_id=country_id,
                epidemic_id=1,
                daily_wise_id=daily_wise_id
            )
            conn.commit()
            print(f"[OK] {country} - {report_date} - {vaccine}")

        except Exception as e:
            print(f"[ERROR] Ligne ignorée : {e}")
            print("→ Ligne concernée :", row)
            conn.rollback()

elif "full_grouped" in CSV_FILE:
    print("📦 Traitement du fichier global par jour")
    for _, row in df.iterrows():
        try:
            continent = row['Continent']
            country = row['Country']
            report_date = datetime.strptime(row['ReportDate'], "%Y-%m-%d")

            continent_id = get_or_create_continent(continent)
            country_id = get_or_create_country(country, continent_id)
            daily_wise_id = insert_daily_wise(report_date, country_id)

            for label in ['TotalDeaths', 'TotalRecovered', 'ActiveCases', 'NewCases', 'NewDeaths', 'NewRecovered']:
                insert_statistic(label, row[label], country_id, 1, daily_wise_id)

            conn.commit()
            print(f"[OK] {country} - {report_date}")

        except Exception as e:
            print(f"[ERROR] Ligne ignorée : {e}")
            print("→ Ligne concernée :", row)
            conn.rollback()


elif "monkeypox" in CSV_FILE:
    print("🦠 Traitement des données Monkeypox")
    for _, row in df.iterrows():
        try:
            country = row['Country']
            report_date = datetime.strptime(row['ReportDate'], "%Y-%m-%d")

            country_id = get_or_create_country(country)
            if not country_id:
                continue

            daily_wise_id = insert_daily_wise(report_date, country_id)

            
            stat_labels = [
                'NewCases',
                'NewDeaths',
                'new_deaths',
                'Tot Cases/1M pop',
                'Deaths/1M pop'
            ]

            for label in stat_labels:
                insert_statistic(label, row.get(label), country_id, 1, daily_wise_id)

            conn.commit()
            print(f"[OK] {country} - {report_date}")

        except Exception as e:
            print(f"[ERROR] Ligne ignorée : {e}")
            print("→ Ligne concernée :", row)
            conn.rollback()


elif "country_wise_latest" in CSV_FILE:
    print("📊 Traitement du fichier country_wise_latest")

    for _, row in df.iterrows():
        try:
            continent = row['Continent']
            country = row['Country']
            report_date = datetime.now()

            continent_id = get_or_create_continent(continent)
            country_id = get_or_create_country(country, continent_id)
            daily_wise_id = insert_daily_wise(report_date, country_id)

            stat_labels = [
                'TotalConfirmed',
                'TotalDeaths',
                'TotalRecovered',
                'ActiveCases',
                'NewCases',
                'NewDeaths',
                'NewRecovered',
                'Recovered / 100 Cases',
                'Deaths / 100 Recovered'
            ]

            for label in stat_labels:
                insert_statistic(label, row.get(label), country_id, 1, daily_wise_id)

            conn.commit()
            print(f"[OK] {country}")

        except Exception as e:
            print(f"[ERROR] Ligne ignorée : {e}")
            print("→ Ligne concernée :", row)
            conn.rollback()


elif "covid_19_clean_complete" in CSV_FILE:
    print("🧼 Traitement du fichier covid_19_clean_complete")

    for _, row in df.iterrows():
        try:
            continent = row['Continent']
            country = row['Country']
            report_date = datetime.strptime(row['ReportDate'], "%Y-%m-%d")

            continent_id = get_or_create_continent(continent)
            country_id = get_or_create_country(country, continent_id)
            daily_wise_id = insert_daily_wise(report_date, country_id)

            stat_labels = [
                'TotalConfirmed',
                'TotalDeaths',
                'TotalRecovered',
                'ActiveCases'
            ]

            for label in stat_labels:
                insert_statistic(label, row.get(label), country_id, 1, daily_wise_id)

            conn.commit()
            print(f"[OK] {country} - {report_date}")

        except Exception as e:
            print(f"[ERROR] Ligne ignorée : {e}")
            print("→ Ligne concernée :", row)
            conn.rollback()


elif "day_wise_cleaned" in CSV_FILE:
    print("📈 Traitement du fichier day_wise_cleaned")

    default_country_name = "World"

    # On récupère ou on crée le pays "World"
    country_id = get_or_create_country(default_country_name)

    for _, row in df.iterrows():
        try:
            report_date = datetime.strptime(row['ReportDate'], "%Y-%m-%d")
            daily_wise_id = insert_daily_wise(report_date, country_id)

            stat_labels = [
                'TotalConfirmed',
                'TotalDeaths',
                'TotalRecovered',
                'ActiveCases',
                'NewCases',
                'NewDeaths',
                'NewRecovered',
                'Recovered / 100 Cases',
                'Deaths / 100 Recovered'
            ]

            for label in stat_labels:
                insert_statistic(label, row.get(label), country_id, 1, daily_wise_id)

            conn.commit()
            print(f"[OK] {report_date}")

        except Exception as e:
            print(f"[ERROR] Ligne ignorée : {e}")
            print("→ Ligne concernée :", row)
            conn.rollback()


elif "usa_county_wise_cleaned" in CSV_FILE:
    print("🗺️ Traitement du fichier usa_county_wise_cleaned")

    for _, row in df.iterrows():
        try:
            country = row['Country']
            province = row.get('Province_State') or None
            lat = row.get('Lat') or None
            lon = row.get('Long_') or None
            report_date = datetime.strptime(row['ReportDate'], "%Y-%m-%d")

            country_id = get_or_create_country(country)
            if not country_id:
                continue

            cur.execute("""
                INSERT INTO daily_wise (
                    date, province, latitude, longitude, country_id, id, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, DEFAULT, FALSE)
                RETURNING id
            """, (report_date, province, lat, lon, country_id))
            daily_wise_id = cur.fetchone()[0]

            for label in ['TotalConfirmed', 'TotalDeaths']:
                insert_statistic(label, row.get(label), country_id, 1, daily_wise_id)

            conn.commit()
            print(f"[OK] {country} - {province} - {report_date}")

        except Exception as e:
            print(f"[ERROR] Ligne ignorée : {e}")
            print("→ Ligne concernée :", row)
            conn.rollback()


elif "worldometer_coronavirus_daily_data_cleaned" in CSV_FILE:
    print("🌐 Traitement du fichier worldometer_coronavirus_daily_data_cleaned")

    for _, row in df.iterrows():
        try:
            country = row['Country']
            report_date = datetime.strptime(row['ReportDate'], "%Y-%m-%d")

            country_id = get_or_create_country(country)
            if not country_id:
                continue

            daily_wise_id = insert_daily_wise(report_date, country_id)

            stat_labels = [
                'NewCases',
                'ActiveCases',
                'TotalDeaths',
                'NewDeaths'
            ]

            for label in stat_labels:
                insert_statistic(label, row.get(label), country_id, 1, daily_wise_id)

            conn.commit()
            print(f"[OK] {country} - {report_date}")

        except Exception as e:
            print(f"[ERROR] Ligne ignorée : {e}")
            print("→ Ligne concernée :", row)
            conn.rollback()


elif "worldometer_data_cleaned" in CSV_FILE:
    print("📊 Traitement du fichier worldometer_data_cleaned (en mode label/value dans statistic)")

    for _, row in df.iterrows():
        try:
            continent = row['Continent']
            country = row['Country']
            population = row.get('Population') or 0
            report_date = datetime.today()

            continent_id = get_or_create_continent(continent)
            country_id = get_or_create_country(country, continent_id)

            # Mise à jour de la population dans la table country
            try:
                cur.execute("UPDATE country SET population = %s WHERE id = %s", (int(population), country_id))
            except Exception as pop_err:
                print(f"⚠️ Erreur update population pour {country}: {pop_err}")

            # Insertion dans daily_wise (date par défaut = aujourd'hui)
            daily_wise_id = insert_daily_wise(report_date, country_id)

            stat_labels = [
                'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths',
                'TotalRecovered', 'NewRecovered', 'ActiveCases',
                'Tot Cases/1M pop', 'Deaths/1M pop',
                'TotalTests', 'Tests/1M pop'
            ]

            for label in stat_labels:
                value = row.get(label)
                insert_statistic(label, value, country_id, 1, daily_wise_id)

            conn.commit()
            print(f"[OK] {country}")

        except Exception as e:
            print(f"[ERROR] Ligne ignorée : {e}")
            print("→ Ligne concernée :", row)
            conn.rollback()

elif "worldometer_coronavirus_summary_data_cleaned" in CSV_FILE:
    print("📋 Traitement du fichier worldometer_coronavirus_summary_data_cleaned")

    for _, row in df.iterrows():
        try:
            continent = row['continent']
            country = row['Country']
            population = row.get('Population') or 0
            report_date = datetime.today()

            continent_id = get_or_create_continent(continent)
            country_id = get_or_create_country(country, continent_id)

            # Mise à jour de la population si elle est fournie
            try:
                cur.execute("UPDATE country SET population = %s WHERE id = %s", (int(population), country_id))
            except Exception as pop_err:
                print(f"⚠️ Erreur update population pour {country}: {pop_err}")

            daily_wise_id = insert_daily_wise(report_date, country_id)

            stat_labels = [
                'NewDeaths',
                'TotalRecovered',
                'ActiveCases',
                'Tot Cases/1M pop',
                'Deaths/1M pop',
                'TotalTest',
                'Tot Test/1M pop'
            ]

            for label in stat_labels:
                insert_statistic(label, row.get(label), country_id, 1, daily_wise_id)

            conn.commit()
            print(f"[OK] {country}")

        except Exception as e:
            print(f"[ERROR] Ligne ignorée : {e}")
            print("→ Ligne concernée :", row)
            conn.rollback()

else:
    print("❌ Fichier non reconnu. Vérifie le nom.")


# Fermeture
cur.close()
conn.close()
print("✅ Import terminé.")
