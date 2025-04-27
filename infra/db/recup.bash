-----------------------------
SCRIPT DE RECUPERATION
-----------------------------

#!/bin/bash

# Configuration - À MODIFIER selon votre environnement
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="mspr"
DB_USER="postgres"
DB_PASSWORD="postgres"
BACKUP_DIR="/chemin/vers/dossier/sauvegardes"

# Vérifiez si un fichier de sauvegarde a été spécifié
if [ -z "$1" ]; then
  echo "Usage: $0 <nom_fichier_sauvegarde>"
  echo "Sauvegardes disponibles:"
  ls -lt $BACKUP_DIR
  exit 1
fi

BACKUP_FILE=$1

# Vérifier que le fichier existe
if [ ! -f "$BACKUP_FILE" ]; then
  echo "Erreur: Le fichier $BACKUP_FILE n'existe pas."
  exit 1
fi

echo "ATTENTION! Cette opération va remplacer la base de données $DB_NAME."
echo "Toutes les données actuelles seront perdues."
read -p "Continuer? (o/n): " CONFIRM

if [ "$CONFIRM" != "o" ]; then
  echo "Restauration annulée."
  exit 0
fi

# Supprimer les connexions à la base pour permettre la restauration
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -p $DB_PORT -d postgres -c "
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = '$DB_NAME'
  AND pid <> pg_backend_pid();"

# Supprimer et recréer la base de données
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -p $DB_PORT -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -p $DB_PORT -d postgres -c "CREATE DATABASE $DB_NAME;"

# Restaurer la sauvegarde
PGPASSWORD=$DB_PASSWORD pg_restore \
  --host=$DB_HOST \
  --port=$DB_PORT \
  --username=$DB_USER \
  --dbname=$DB_NAME \
  --verbose \
  $BACKUP_FILE

# Vérifier que la restauration a fonctionné
if [ $? -eq 0 ]; then
  echo "Restauration réussie à partir de: $BACKUP_FILE"
else
  echo "ERREUR: La restauration a échoué!"
  exit 1
fi
