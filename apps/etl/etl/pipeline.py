from etl.loader import DataLoader
from etl.transformer import DataTransformer
from configapp import DEFAULT_OUTPUT_DIR

class ETLPipeline:
    def __init__(self, output_dir=DEFAULT_OUTPUT_DIR):
        self.output_dir = output_dir
        self.loader = DataLoader()
        self.transformer = DataTransformer(output_dir=output_dir)
        self.datasets = {}
        self.transformed_datasets = {}
    
    def run(self, file_info_list):
        """Execute le pipeline ETL complet sur une liste de fichiers"""
        # Étape 1: Extraction - Charger les fichiers
        self.datasets = self.loader.load_files(file_info_list)
        
        if not self.datasets:
            print("Aucun dataset n'a été chargé. Le pipeline s'arrête.")
            return False
        
        # Étape 2: Transformation - Nettoyer et standardiser les données
        self.transformed_datasets = self.transformer.transform_and_save(self.datasets)
        
        # Retourner le statut de succès
        return len(self.transformed_datasets) > 0
    
    def run_with_predefined_paths(self, file_paths):
        """Execute le pipeline ETL avec des chemins de fichiers prédéfinis"""
        # Étape 1: Extraction - Charger les fichiers
        self.datasets = self.loader.load_multiple_csv(file_paths)
        
        if not self.datasets:
            print("Aucun dataset n'a été chargé. Le pipeline s'arrête.")
            return False
        
        # Étape 2: Transformation - Nettoyer et standardiser les données
        self.transformed_datasets = self.transformer.transform_and_save(self.datasets)
        
        # Retourner le statut de succès
        return len(self.transformed_datasets) > 0
    
    def get_original_datasets(self):
        """Renvoie les datasets originaux"""
        return self.datasets
    
    def get_transformed_datasets(self):
        """Renvoie les datasets transformés"""
        return self.transformed_datasets