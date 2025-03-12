#!/bin/bash

# Chemin du fichier .env
ENV_FILE="../.env"

# Vérifier si le fichier .env existe déjà
if [ -f "$ENV_FILE" ]; then
    echo "🔹 Le fichier .env existe déjà."
    echo "Voulez-vous le recréer ? (y/n)"
    read -r RECREATE_ENV
    if [ "$RECREATE_ENV" != "y" ]; then
        echo "✅ Utilisation du fichier .env existant."
        exit 0
    fi
fi

# Demander à l'utilisateur de renseigner les valeurs sensibles
echo "💾 Configuration de l'environnement Docker"
echo "Entrez le mot de passe PostgreSQL :"
read -s POSTGRES_PASSWORD

echo "Entrez le port PostgreSQL (par défaut : 5432) :"
read -r POSTGRES_PORT
POSTGRES_PORT=${POSTGRES_PORT:-5432} # Utiliser 5432 si l'utilisateur ne remplit pas

echo "Entrez le nom de la base de données (par défaut : mspr) :"
read -r POSTGRES_DB
POSTGRES_DB=${POSTGRES_DB:-mspr}

# Écriture des valeurs dans le fichier .env
cat <<EOF >"$ENV_FILE"
# Configuration PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_DB=$POSTGRES_DB
POSTGRES_HOST=db
POSTGRES_PORT=$POSTGRES_PORT

# Autres paramètres
DEBUG=True
LOG_LEVEL=DEBUG
EOF

echo "✅ Fichier .env généré avec succès !"
