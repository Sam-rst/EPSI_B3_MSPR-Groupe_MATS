from pipelines.export import Export
from pipelines.transform import DataTransformer
import os
from configapp import DEFAULT_OUTPUT_DIR

class ETLPipeline:
    def __init__(self, output_dir=DEFAULT_OUTPUT_DIR):
        self.output_dir = output_dir
        self.exporter = Export()
        self.transformer = DataTransformer(output_dir=output_dir)
        self.datasets = {}
        self.transformed_datasets = {}
    
    def run(self, input_files, on_progress=None):
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
        
        total_files = len(self.datasets)
        self.transformed_datasets = {}

        for i, (name, df) in enumerate(self.datasets.items()):
            transformed_df = self.transformer.transform_dataframe(df, dataset_name=name)
            self.transformed_datasets[name] = transformed_df

            output_path = os.path.join(self.output_dir, f"{name}_cleaned.csv")
            transformed_df.to_csv(output_path, index=False)
            print(f"Fichier sauvegardé: {output_path}")

            if on_progress:
                on_progress(i + 1, total_files)

        return len(self.transformed_datasets) > 0