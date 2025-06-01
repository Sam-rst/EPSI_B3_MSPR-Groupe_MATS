import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.data_manager import DataManager
from scripts.multi_target_predictor import MultiTargetPredictor


dm = DataManager("output/data")
df = dm.load_all()

print(df[["Country", "ReportDate", "total_vaccinations"]].head())


mt = MultiTargetPredictor(df, prediction_length=90)

# print("--- France, NewCases, 14 j ---")
# print(mt.predict("France", target="NewCases", horizon=14))

# print("--- France, TotalDeaths, 60 j ---")
# print(mt.predict("France", target="TotalDeaths", horizon=60))

# print("--- France, TotalRecovered, 30 j ---")
# print(mt.predict("France", target="TotalRecovered", horizon=30))

# print("--- Germany, NewCases, 14 j ---")
# print(mt.predict("Germany", target="NewCases", horizon=14))

# print("--- Germany, TotalDeaths, 60 j ---")
# print(mt.predict("Germany", target="TotalDeaths", horizon=60))

# print("--- Germany, TotalRecovered, 30 j ---")
# print(mt.predict("Germany", target="TotalRecovered", horizon=30))


print(mt.predict("Germany", target="total_vaccinations", horizon=30))