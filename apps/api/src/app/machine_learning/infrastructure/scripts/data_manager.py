import os, glob, pandas as pd


COUNTRY_ALIASES = {
    "Country/Other": "Country",
    "location": "Country",
    "Province_State": "Country",
    "Country_Region": "Country",
}

COLUMN_ALIASES = {
    "TotalVaccination": "total_vaccinations",
    "total_vaccinations_per_hundred": "total_vaccinations_pct",
}

class DataManager:
    """
    Fusionne tous les CSV de `cleaned_dir` en un DataFrame unique.
    Résultat accessible via self.df ou load_all().
    """

    def __init__(self, cleaned_dir="data/cleaned"):
        self.cleaned_dir = cleaned_dir
        self.df = None

    def _harmonise(self, df: pd.DataFrame) -> pd.DataFrame | None:
        # (A) pays
        for alias, std in COUNTRY_ALIASES.items():
            if alias in df.columns and "Country" not in df.columns:
                df = df.rename(columns={alias: std})
        if "Country" not in df.columns:
            return None 

        if "date" in df.columns and "ReportDate" not in df.columns:
            df = df.rename(columns={"date": "ReportDate"})
        if "ReportDate" in df.columns:
            df["ReportDate"] = pd.to_datetime(df["ReportDate"])

        for old, new in COLUMN_ALIASES.items():
            if old in df.columns and new not in df.columns:
                df = df.rename(columns={old: new})

        return df

    def load_all(self, pivot_file: str = None) -> pd.DataFrame:
        # Fichier pivot
        if pivot_file is None:
            pivot = os.path.join(self.cleaned_dir, "covid_19_clean_complete_cleaned.csv")
        else:
            pivot = pivot_file

        if not os.path.exists(pivot):
            raise FileNotFoundError(f"Le fichier pivot {pivot} n'existe pas")

        main = pd.read_csv(pivot)
        main = self._harmonise(main)

        # Parcours des autres CSV et fusion
        for path in glob.glob(os.path.join(self.cleaned_dir, "*.csv")):
            if path == pivot:
                continue

            extra = pd.read_csv(path)
            extra = self._harmonise(extra)
            if extra is None:
                print(f"⚠️  {os.path.basename(path)} ignoré : pas de colonne pays")
                continue

            # Cas spécial : vaccination par fabricant
            if path.endswith("_by_manufacturer_cleaned.csv"):
                extra = (
                    extra.groupby(["Country", "ReportDate"], as_index=False)
                        ["total_vaccinations"].sum()
                )

            join_cols = (["Country", "ReportDate"]
                        if "ReportDate" in extra.columns else ["Country"])

            main = main.merge(extra, on=join_cols, how="outer",
                            suffixes=("", "_dup"))

        main = main.loc[:, ~main.columns.str.endswith("_dup")]

        main = main.sort_values(["Country", "ReportDate"])
        if "NewCases" not in main.columns and "TotalConfirmed" in main.columns:
            main["NewCases"] = (main.groupby("Country")["TotalConfirmed"]
                                    .diff().fillna(0))

        if "total_vaccinations" in main.columns:
            main["total_vaccinations"] = (
                main.groupby("Country")["total_vaccinations"]
                    .ffill().interpolate().fillna(0)
            )

            first_date_map = (
                main.loc[main["total_vaccinations"] > 0]
                    .groupby("Country")["ReportDate"]
                    .min()
                    .apply(pd.Timestamp)           # assure le dtype datetime64
                    .to_dict()
            )

            main["first_vacc_date"] = main["Country"].map(first_date_map)

            mindate = main["ReportDate"].min()
            main["first_vacc_date"] = main["first_vacc_date"].fillna(mindate)

            main = main[main["ReportDate"] >= main["first_vacc_date"]]

            main = main.drop(columns=["first_vacc_date"])
        self.df = main
        return main
