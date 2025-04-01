import os
from datetime import datetime
from configapp import SUPPORTED_FORMATS

class FileInfo:
    def __init__(self, file_path):
        self.path = file_path
        self.name = os.path.basename(file_path) if file_path else ""
        self.ext = os.path.splitext(file_path)[1].lower() if file_path else ""
        self.selected = True
        
        # Valeurs par défaut
        self.format_type = "unknown"
        self.format_display = "???"
        self.format_color = "#999999"
        self.size_bytes = 0
        self.modified_date = datetime.now()
        
        # Déterminer le type et le format
        self._set_format_info()
        
        # Charger les informations du fichier si le chemin existe
        if file_path and os.path.exists(file_path):
            self._load_file_stats()
    
    def _set_format_info(self):
        for format_type, info in SUPPORTED_FORMATS.items():
            if self.ext in info["extensions"]:
                self.format_type = format_type
                self.format_display = info["display_name"]
                self.format_color = info["color"]
                return
    
    def _load_file_stats(self):
        try:
            self.size_bytes = os.path.getsize(self.path)
            self.modified_date = datetime.fromtimestamp(os.path.getmtime(self.path))
        except (FileNotFoundError, PermissionError) as e:
            print(f"Erreur lors du chargement des stats du fichier: {str(e)}")
            self.size_bytes = 0
            self.modified_date = datetime.now()
    
    @property
    def size_kb(self):
        return self.size_bytes // 1024
    
    @property
    def size_display(self):
        if self.size_bytes < 1024:
            return f"{self.size_bytes} B"
        elif self.size_bytes < 1024 * 1024:
            return f"{self.size_kb} Ko"
        else:
            return f"{self.size_bytes / (1024 * 1024):.1f} Mo"
    
    @property
    def date_display(self):
        if self.modified_date:
            return self.modified_date.strftime('%d/%m/%Y')
        return ""
    
    @property
    def is_large_file(self):
        return self.size_kb > 1000
    
    @property
    def size_color(self):
        return "#4A7CFF" if self.is_large_file else "#9370DB"  # Bleu ou violet
    
    def __str__(self):
        return f"{self.name} ({self.format_display}, {self.size_display})"