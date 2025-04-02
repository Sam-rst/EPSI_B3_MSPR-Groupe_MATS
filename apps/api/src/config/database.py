import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


class Database:
    def __init__(self):
        """Initialise la connexion à la base de données en chargeant les variables d'environnement."""
        # Charger les variables d'environnement depuis un fichier .env (si présent)
        load_dotenv()

        # Récupérer les valeurs des variables d'environnement
        db_user = os.getenv("POSTGRES_USER")
        db_password = os.getenv("POSTGRES_PASSWORD")
        db_host = os.getenv("POSTGRES_HOST", "localhost")
        db_port = os.getenv("POSTGRES_PORT", "5432")
        db_name = os.getenv("POSTGRES_DB")

        # Construire l'URL de connexion à la base de données
        database_url = (
            f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        self._engine = create_engine(database_url)
        self._SessionLocal = sessionmaker(
            autocommit=True, autoflush=True, bind=self.engine
        )

    def get_db(self):
        """
        Fournit une session de base de données.
        À utiliser avec `Depends()` dans FastAPI ou via `with db.get_db() as session:`.
        """
        db = self._SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @property
    def engine(self):
        """Retourne l'engine SQLAlchemy (utile pour migrations ou tests manuels)."""
        return self._engine

    def create_engine(self, database_url):
        """Définit l'engine SQLAlchemy (utile pour les tests)."""
        # Vérifier si l'engine a été correctement créé
        engine = create_engine(database_url)
        if engine:
            print("******** Engine created successfully ********")
            self._engine = engine
        else:
            raise Exception("Failed to create engine")

    def get_session(self):
        """Fournit une session de base de données."""
        return self._SessionLocal()


db = Database()
