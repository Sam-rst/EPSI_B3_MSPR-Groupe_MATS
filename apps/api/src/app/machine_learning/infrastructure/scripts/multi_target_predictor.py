# scripts/multi_target_predictor.py
from autogluon.timeseries import TimeSeriesPredictor, TimeSeriesDataFrame
from pathlib import Path
import os, shutil

FAST_MODELS = {
    "Naive": {}, "SeasonalNaive": {}, "ETS": {}, "Theta": {},
    "RecursiveTabular": {}, "DirectTabular": {},
}

class MultiTargetPredictor:
    def __init__(self, dataframe, model_root="models", prediction_length=90):
        self.df = dataframe
        self.model_root = model_root
        self.prediction_length = prediction_length

        self.ts_df = TimeSeriesDataFrame.from_data_frame(
            dataframe, id_column="Country", timestamp_column="ReportDate"
        )
        self.cache = {}

    def _path(self, target):        
        return os.path.join(self.model_root, target)

    def _ensure(self, target):
        path = self._path(target)

        # charge si déjà présent
        if Path(path).exists():
            pred = TimeSeriesPredictor.load(path)
            if pred.prediction_length == self.prediction_length:
                self.cache[target] = pred
                return

        # sinon entraîne
        print(f"🔄 Entraînement du modèle « {target} » …")
        pred = TimeSeriesPredictor(
            target=target, prediction_length=self.prediction_length, freq="1D"
        )
        pred.fit(self.ts_df, presets="medium_quality", hyperparameters=FAST_MODELS)
        pred.save()

        
        ag_dirs = [d for d in os.listdir("AutogluonModels") if d.startswith("ag-")]
        ag_dirs.sort(reverse=True)
        saved_dir = os.path.join("AutogluonModels", ag_dirs[0])

        os.makedirs(self.model_root, exist_ok=True)
        shutil.copytree(saved_dir, path, dirs_exist_ok=True)

        self.cache[target] = pred


    def predict(self, country, target, horizon):
        self._ensure(target)

        if country not in self.ts_df.item_ids:
            raise ValueError(f"⛔ « {country} » absent ou série trop courte.")
        if horizon > self.prediction_length:
            raise ValueError("horizon > prediction_length")

        fc = self.cache[target].predict(self.ts_df).loc[country]
        return fc.iloc[:horizon]
