# Base image officielle Python
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy code
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ .

# Commande par défaut à l'exécution
CMD ["python", "main.py"]
