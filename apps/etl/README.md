# Analyze IT - Solution ETL

[⬅️ Retour](/README.md)

<p align="center">
  <a href="#Aperçu">Aperçu</a> •
  <a href="#Fonctionnalités">Fonctionnalités</a> •
  <a href="#Installation">Installation</a> •
  <a href="#Utilisation">Utilisation</a> •
  <a href="#Architecture">Architecture</a> •
  <a href="#Documentation-technique">Documentation Technique</a> •
</p>

## Aperçu

Analyze IT est une application ETL (Extract, Transform, Load) développée pour standardiser et nettoyer les données épidémiologiques provenant de diverses sources. Face à l'hétérogénéité des formats et conventions utilisés pour publier les données COVID-19, cette solution facilite l'intégration et l'analyse en proposant un pipeline complet de traitement.

## Fonctionnalités

- ✨ **Interface graphique intuitive** avec support du glisser-déposer
- 📥 **Extraction** de données depuis plusieurs fichiers CSV
- 🔄 **Transformation** avec standardisation des noms de colonnes, formats de dates et noms de pays
- 🧹 **Nettoyage** intelligent des valeurs manquantes selon le type de données
- 📤 **Export** des données nettoyées au format CSV
- 💾 **Chargement** dans une base de données PostgreSQL
- ⚙️ **Configuration flexible** via un système de mapping YAML

## Installation

### Prérequis

- Python 3.10+
- Docker
- DBeaver ou PGAdmin

### Installation standard

```bash
# Installer les dépendances
pip install -r requirements.txt
```


## Utilisation

Démarrage de l'application
```bash
# A la racine du projet ETL (apps/etl/)
python main.py
```
**Interface utilisateur**
L'interface d'Analyze IT est conçue pour être intuitive et accessible même aux utilisateurs non-techniques:

**Zone d'importation des fichiers**

Utilisez le bouton "Ajouter des fichiers CSV" pour sélectionner vos données
Ou glissez-déposez directement vos fichiers dans l'application
Formats supportés: *CSV*


**Gestion des fichiers**

Visualisez les fichiers importés avec leurs informations (taille, date, format)
Cochez/décochez les fichiers à inclure dans le traitement
Supprimez des fichiers de la liste si nécessaire


**Configuration**

Définissez le répertoire de sortie pour les fichiers traités
Par défaut: dossier ./cleaned/ dans le répertoire de l'application

**Transformation**

1. *Vérifier et sélectionner les fichiers*
Les fichiers apparaissent dans la liste centrale avec des informations détaillées. Assurez-vous que les fichiers que vous souhaitez traiter sont bien cochés.
2. *Lancer le traitement*
Cliquez sur le bouton "Traiter les fichiers" pour démarrer le pipeline ETL. L'application affichera la progression et les éventuelles erreurs dans la barre d'état.
3. *Charger dans PostgreSQL* (optionnel mais recommandé)
Après le traitement, cliquez sur "Charger dans PostgreSQL" pour ouvrir la boîte de dialogue de connexion:

- Testez la connexion avec le bouton "Tester connexion"
- Lancez le chargement avec "Charger dans PostgreSQL"

**Visualisation avec Metabase**

Une fois les données chargées dans PostgreSQL, vous pouvez utiliser Metabase pour créer des tableaux de bord interactifs:

1. Connectez Metabase à votre base de données PostgreSQL
2. Utilisez l'interface de création de tableaux de bord
3. Exploitez la structure standardisée pour créer des visualisations pertinentes
## Architecture

![Schéma ](docs/architecture/img/ArchitectureETL.svg)

## Documentation Technique

https://www.canva.com/design/DAGj5AJliDw/FhhWY4X7QrvmJrBGfVMY1w/edit?utm_content=DAGj5AJliDw&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton