from pipelines.export import Export
from pipelines.transform import DataTransformer
from configapp import DEFAULT_OUTPUT_DIR

class ETLPipeline:
    def __init__(self, output_dir=DEFAULT_OUTPUT_DIR):
        self.output_dir = output_dir
        self.exporter = Export()
        self.transformer = DataTransformer(output_dir=output_dir)
        self.datasets = {}
        self.transformed_datasets = {}
    
    def run(self, input_files):
        """Execute le pipeline ETL
        
        Args:
            input_files: Peut être une liste d'objets FileInfo ou une liste de chemins (str)
        """
        if input_files and isinstance(input_files[0], str):
            self.datasets = self.exporter.load_multiple_csv(input_files)
        else:
            self.datasets = self.exporter.load_files(input_files)
        
        if not self.datasets:
            print("Aucun dataset n'a été chargé. Le pipeline s'arrête.")
            return False
        
        self.transformed_datasets = self.transformer.transform_and_save(self.datasets)
        return len(self.transformed_datasets) > 0