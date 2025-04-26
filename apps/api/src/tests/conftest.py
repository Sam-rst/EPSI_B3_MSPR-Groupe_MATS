import sys
from pathlib import Path

# Obtenir le chemin vers la racine du projet (apps/api/)
api_root = Path(__file__).parent.parent

# Ajouter le répertoire principal au PYTHONPATH
sys.path.insert(0, str(api_root))