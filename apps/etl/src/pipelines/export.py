import pandas as pd
import os


class Export:
    def __init__(self):
        self.datasets = {}

    def load_csv(self, file_path, dataset_name=None):
        """Charge un fichier CSV dans un DataFrame"""
        try:
            # Si aucun nom de dataset n'est fourni, utiliser le nom du fichier
            if dataset_name is None:
                dataset_name = os.path.basename(file_path).split(".")[0]

            print(f"Chargement du fichier: {file_path}")
            df = pd.read_csv(file_path)  # charge le fichier dans un dataframe
            self.datasets[dataset_name] = (
                df  # Stock le dataframe dans le dictionnaire attribué
            )
            print(
                f"Fichier chargé avec succès: {dataset_name} ({len(df)} lignes, {len(df.columns)} colonnes)"
            )
            return df
        except Exception as e:
            print(f"Erreur lors du chargement du fichier {file_path}: {str(e)}")
            return None

    def load_multiple_csv(self, file_paths):
        """Charge plusieurs fichiers CSV à partir d'un dictionnaire"""
        success_count = 0
        for name, path in file_paths.items():
            df = self.load_csv(path, name)
            if df is not None:
                success_count += 1

        print(f"{success_count}/{len(file_paths)} fichiers chargés avec succès")
        return self.datasets

    def load_files(self, file_info_list):
        """Charge des fichiers à partir d'une liste d'objets FileInfo provenant de l'UI"""
        file_paths = {}

        for file_info in file_info_list:
            if file_info.selected:  # Ne charger que les fichiers selectionnes
                if file_info.format.lower() in [
                    ".csv",
                    "csv",
                ]:  # Ne traite que les fichiers CSV
                    name = os.path.basename(file_info.path).split(".")[0]
                    file_paths[name] = file_info.path

        return self.load_multiple_csv(file_paths)

    def get_datasets(self):
        """Renvoie les datasets chargés"""
        return self.datasets
