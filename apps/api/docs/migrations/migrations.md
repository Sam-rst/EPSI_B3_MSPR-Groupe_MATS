# 📦 Gestion des Migrations avec Alembic

[⬅️ Retour](../../README.md)

Documentation rédigée par Samuel RESSIOT

---

## 📝 Introduction

Bienvenue dans le guide des migrations de base de données du projet. Ce document explique **comment utiliser Alembic**, l'outil officiel de migration de schéma pour SQLAlchemy.

---

## 🔧 Prérequis

- Python installé (version >= 3.8)
- Base de données PostgreSQL configurée
- Fichier `.env` contenant les variables suivantes (à la racine du projet) :

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=your_db_name
```

- Alembic installé :

```bash
pip install alembic python-dotenv
```

---

## 📁 Structure de projet attendue

```txt
apps/
├── api/
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   ├── README
│   │   ├── versions/
│   │   │   ├── <timestamp>_<description>.py
│   │   │   └── ...
│   │   └── __pycache__/
│   ├─ docs/
│   ├── src/
│   └── tests/
│   └── alembic.ini
├── ...
config/
docs/
infra/
.env
```

---

## 🚀 Commandes essentielles

### 🔍 Vérifier la connexion à la base
>
> Automatiquement testé dans `alembic/env.py` à chaque commande.

---

### 📄 Générer une nouvelle migration

```bash
alembic revision --autogenerate -m "ajout d'une modification de la base"
```

- Compare les modèles SQLAlchemy à l’état de la base.
- Crée un fichier dans `alembic/versions/`.

---

### ⬆️ Appliquer toutes les migrations à la base

```bash
alembic upgrade head
```

- Applique toutes les migrations jusqu’à la dernière (`head`).

---

### 🔽 Revenir à la migration précédente

```bash
alembic downgrade -1
```

- Utile pour annuler une migration tout juste appliquée.

---

### 📌 Marquer la base comme à jour (sans appliquer les scripts)

```bash
alembic stamp head
```

- Attention : utile seulement si la base est déjà alignée mais que les métadonnées Alembic sont manquantes.

---

### 📜 Afficher l'historique des migrations

```bash
alembic history --verbose
```

---

### ❓ Voir le statut actuel

```bash
alembic current
```

- Montre la version actuelle de la base (présente dans la table `alembic_version`).

---

## ✅ Bonnes pratiques

- Toujours tester les modèles avec un script indépendant si nécessaire.
- Ne jamais modifier une migration déjà appliquée — créer une nouvelle migration.
- Ne jamais versionner `.env` dans Git :

  ```bash
  echo ".env" >> .gitignore
  ```
