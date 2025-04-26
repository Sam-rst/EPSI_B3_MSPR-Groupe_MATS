"""
Module de connexion à PostgreSQL pour la gestion des utilisateurs.
"""

import os
import psycopg2
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()


class PostgresConnector:
    def __init__(self):
        # Récupérer les informations de connexion depuis les variables d'environnement
        # Avec des valeurs par défaut pour le développement local
        self.connection_params = {
            "host": os.environ.get(
                "ETL_POSTGRES_HOST", "localhost"
            ),  # Utiliser localhost par défaut
            "database": os.environ.get("ETL_POSTGRES_DB", "mspr"),
            "user": os.environ.get("ETL_POSTGRES_USER", "postgres"),
            "password": os.environ.get("ETL_POSTGRES_PASSWORD", "postgres"),
            "port": int(os.environ.get("ETL_POSTGRES_PORT", 5432)),
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
            return True
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête: {e}")
            self.connection.rollback()
            return False

    def fetch_one(self, query, params=None):
        """Exécute une requête SQL et renvoie une ligne"""
        if not self.connection or self.connection.closed:
            if not self.connect():
                return None

        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête: {e}")
            return None

    def fetch_all(self, query, params=None):
        """Exécute une requête SQL et renvoie toutes les lignes"""
        if not self.connection or self.connection.closed:
            if not self.connect():
                return None

        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête: {e}")
            return None

    def initialize_users_table(self):
        """Crée la table users si elle n'existe pas"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            login VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(64) NOT NULL,
            role VARCHAR(50) NOT NULL,
            region VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        return self.execute_query(create_table_query)
