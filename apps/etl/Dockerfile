# Utiliser une image Python comme base
FROM python:3.10

# Installer gettext pour envsubst
RUN apt-get update && apt-get install -y gettext

# Définir le répertoire de travail
WORKDIR /app

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Exposer le port de FastAPI
EXPOSE 8000

# Commande d'exécution
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
