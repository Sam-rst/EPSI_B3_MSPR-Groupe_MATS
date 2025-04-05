import pandas as pd
import os

class DataTransformer:
    def __init__(self, output_dir="./cleaned/"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Dictionnaire de standardisation des noms de colonnes
        self.rename_dict = {
            # Country
            "Country/Region": "Country",
            "Country_Region": "Country",
            "country": "Country",
            "location": "Country",
            "Province/State": "Province",
            "contient": "Continent",
            "WHO Region": "Continent",
            # Confirmed
            "Confirmed": "TotalConfirmed",
            # Deaths
            "Deaths": "TotalDeaths",
            "cumulative_total_deaths": "TotalDeaths",
            "New deaths": "NewDeaths",
            "daily_new_deaths": "NewDeaths",
            "total_deaths": "NewDeaths",
            "total_deaths_per_million": "Deaths/1M pop",
            "total_deaths_per_1m_population": "Deaths/1M pop",
            # Recovered
            "Recovered": "TotalRecovered",
            "New recovered": "NewRecovered",
            "total_recovered": "TotalRecovered",
            "Active": "ActiveCases",
            "active_cases": "ActiveCases",
            "cumulative_total_cases": "TotalCases",
            "total_confirmed": "TotalCases",
            "New cases": "NewCases",
            "daily_new_cases": "NewCases",
            "total_cases": "NewCases",
            "total_cases_per_million": "Tot Cases/1M pop",
            "total_cases_per_1m_population": "Tot Cases/1M pop",
            # Vaccin
            "vaccine": "Vaccine",
            "total_vaccinations" : "TotalVaccination",
            # Test
            "total_tests": "TotalTest",
            "total_tests_per_1m_population" : "Tot Test/1M pop",
            # Date
            "Date": "ReportDate",
            "date": "ReportDate",
            # Population 
            "population": "Population",
        }
        
        # Colonnes à supprimer
        self.columns_to_drop = [
            "UID", "iso2", "iso3", "code3", "iso_code", "FIPS", "Admin2", "Combined_Key", 
            "new_cases", "new_cases_per_million", "new_deaths_per_million", "new_cases_smoothed", 
            "new_deaths_smoothed", "new_cases_smoothed_per_million", "new_deaths_smoothed_per_million", 
            "serious_or_critical", "Deaths / 100 Cases", "Recovered / 100 Cases,Deaths / 100 Recovered", 
            "Confirmed last week", "1 week change", "1 week % increase", "Serious,Critical", "No. of countries"
        ]

        self.country_harmonization = {
            "Hong Kong": ["Hong-Kong", "China Hong-Kong"],
            "Bosnia and Herzegovina": ["Bosnia And Herzegovina"],
            "Central African Republic": ["CAR"],
            "Democratic Republic of the Congo": [
                "Congo (Kinshasa)", "Congo (Brazzaville)", "Congo",
                "Democratic Republic Of The Congo", "DRC"
            ],
            "Ivory Coast": ["cote d'ivoire"],
            "Curaçao": ["Curacao"],
            "Dominican Republic": ["Dominica"],
            "European Union": ["Europe"],
            "Falkland Islands": ["Faeroe Islands", "Falkland Islands Malvinas"],
            "Isle of Man": ["Isle Of Man"],
            "Saint Kitts and Nevis": ["Saint Kitts And Nevis"],
            "Saint Vincent and the Grenadines": ["Saint Vincent And the Grenadines", "St. Vincent Grenadines"],
            "Sao Tome and Principe": ["Sao Tome And Principe"],
            "Taiwan": ["Taiwan*"],
            "Timor-Leste": ["Timor Leste"],
            "Trinidad and Tobago": ["Trinidad And Tobago"],
            "Turks and Caicos": ["Turks And Caicos"],
            "United Arab Emirates": ["UAE"],
            "United States": ["US", "USA"],
            "Vietnam": ["Viet Nam"]
        }
    
    def check_duplicate_columns(self, df):
        """Vérifie et renvoie les colonnes en double dans un DataFrame"""
        duplicates = df.columns[df.columns.duplicated()].tolist()
        return duplicates
    
    def fix_duplicate_columns(self, df):
        """Résout les problèmes de colonnes en double"""
        duplicates = self.check_duplicate_columns(df)
        if duplicates:
            print(f"Colonnes en double détectées: {duplicates}")
            # Renommer les colonnes en double pour les rendre uniques
            new_columns = []
            seen = set()
            for col in df.columns:
                if col in seen:
                    # Trouver un nouveau nom unique pour cette colonne
                    i = 1
                    new_col = f"{col}_{i}"
                    while new_col in seen:
                        i += 1
                        new_col = f"{col}_{i}"
                    new_columns.append(new_col)
                    seen.add(new_col)
                    print(f"  - Colonne dupliquée '{col}' renommée en '{new_col}'")
                else:
                    new_columns.append(col)
                    seen.add(col)
            
            # Appliquer les nouveaux noms de colonnes
            df.columns = new_columns
        return df
    
    def clean_dataframe(self, df):
        """Nettoie un DataFrame en gérant les valeurs manquantes"""
        df = df.copy()
        for col in df.columns:
            if pd.api.types.is_datetime64_dtype(df[col]):
                df.loc[:, col] = df[col].fillna(pd.NaT)         # Laisse les dates manquantes comme NaT
            elif pd.api.types.is_numeric_dtype(df[col]):
                df.loc[:, col] = df[col].fillna(0)              # Remplace les NaN numériques par 0
            else:
                df.loc[:, col] = df[col].fillna("Unknown")      # Remplace les NaN texte par "Unknown"
        return df
    
    def standardize_dates(self, df):
        """Standardise les dates dans le DataFrame"""
        if "ReportDate" in df.columns:
            df["ReportDate"] = pd.to_datetime(df["ReportDate"], errors='coerce')
            df["ReportDate"] = df["ReportDate"].dt.strftime('%Y-%m-%d')
            df["ReportDate"] = pd.to_datetime(df["ReportDate"], format="%Y-%m-%d", errors='coerce')
        return df
    
    def harmonize_countries(self, df):
        """Standardise les noms des pays selon le dictionnaire d'harmonisation."""
        if "Country" in df.columns:
            reverse_map = {}
            for standard_name, synonyms in self.country_harmonization.items():
                for synonym in synonyms:
                    reverse_map[synonym.lower()] = standard_name

            # Appliquer l'harmonisation en ignorant la casse
            df["Country"] = df["Country"].apply(
                lambda x: reverse_map.get(x.strip().lower(), x) if isinstance(x, str) else x
            )
        return df

    def transform_dataframe(self, df, dataset_name=""):
        """Applique toutes les transformations à un DataFrame"""
        print(f"Transformation du dataset: {dataset_name}")
        
        # Vérifier et corriger les colonnes en double
        df = self.fix_duplicate_columns(df)
        
        # Standardiser les noms de colonnes
        df.rename(columns=self.rename_dict, inplace=True)
        
        # Vérifier à nouveau pour les colonnes en double après le renommage
        df = self.fix_duplicate_columns(df)
        
        # Standardisation des dates
        df = self.standardize_dates(df)

        # Standardiser les valeurs du champ Country
        df = self.harmonize_countries(df)

        # Suppression des colonnes inutiles
        for col in self.columns_to_drop:
            if col in df.columns:
                df.drop(columns=[col], inplace=True)
        
        # Gestion des valeurs manquantes
        df = self.clean_dataframe(df)
        
        print(f"Transformation terminée pour: {dataset_name}")
        return df
    

    def transform_and_save(self, datasets):
        """Transforme et sauvegarde plusieurs DataFrames"""
        transformed_datasets = {}
        
        for name, df in datasets.items():
            transformed_df = self.transform_dataframe(df, name)
            transformed_datasets[name] = transformed_df
            
            # Sauvegarde du fichier nettoyé
            output_path = f"{self.output_dir}{name}_cleaned.csv"
            transformed_df.to_csv(output_path, index=False)
            print(f"Fichier sauvegardé: {output_path}")
        
        return transformed_datasets
        
    def combine_datasets(self, datasets, output_filename="combined_data.csv"):
        """Combine plusieurs datasets en un seul fichier"""
        # Cette fonction est à compléter selon vos besoins spécifiques
        # Exemple simple: concaténer tous les datasets qui ont les mêmes colonnes
        # TODO: implémenter la logique de combinaison
        pass