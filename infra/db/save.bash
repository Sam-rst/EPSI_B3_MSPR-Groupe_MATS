--------------------------
SCRIPT DE SAUVEGARDE
--------------------------

#!/bin/bash

# Configuration - À MODIFIER selon votre environnement
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="mspr"
DB_USER="postgres"
DB_PASSWORD="postgres"
BACKUP_DIR="/chemin/vers/dossier/sauvegardes"
DAYS_TO_KEEP=7
DATE_FORMAT=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${DATE_FORMAT}.backup"

# Créer le répertoire de sauvegarde s'il n'existe pas
mkdir -p $BACKUP_DIR

# Exécution de la sauvegarde
PGPASSWORD=$DB_PASSWORD pg_dump \
    --host=$DB_HOST \
    --port=$DB_PORT \
    --username=$DB_USER \
    --format=custom \
    --verbose \
    --file=$BACKUP_FILE \
    $DB_NAME

# Vérifier que la sauvegarde a fonctionné
if [ $? -eq 0 ]; then
    echo "Sauvegarde réussie: $BACKUP_FILE"

    # Suppression des sauvegardes plus anciennes que X jours
    find $BACKUP_DIR -name "$DB_NAME*.backup" -mtime +$DAYS_TO_KEEP -delete
    echo "Anciennes sauvegardes nettoyées (plus de $DAYS_TO_KEEP jours)"
else
    echo "ERREUR: La sauvegarde a échoué!"
    exit 1
fi
