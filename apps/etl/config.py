# Informations sur l'application
APP_TITLE = "Analyze IT CSV analyzer"
APP_VERSION = "1.0.0"
DEFAULT_SIZE = "900x600"

# Formats de fichiers supportés
SUPPORTED_FORMATS = {
    "csv": {
        "extensions": [".csv"],
        "description": "Fichiers CSV",
        "color": "#FFA500",
        "display_name": "CSV"
    },
    "excel": {
        "extensions": [".xlsx", ".xls"],
        "description": "Fichiers Excel",
        "color": "#00AA00",
        "display_name": "XLSX"
    }
}

# Chemins des dossiers
DEFAULT_EXPORT_FOLDER = "exports"
DEFAULT_TEMP_FOLDER = "temp"

# Configuration ETL
ETL_BATCH_SIZE = 5000
DEFAULT_ENCODING = "utf-8"
ALTERNATIVE_ENCODINGS = ["latin-1", "cp1252"]
CSV_DELIMITERS = [",", ";", "\t", "|"]