import pandas as pd
from pipelines.extract import extract_csv
from pipelines.transform import transform_data

def test_extract_csv():
    file_path = "tests/sample.csv"
    with open(file_path, "w") as f:
        f.write("id,name,age\n1,John,30\n2,Alice,25")

    df = extract_csv(file_path)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 3)

def test_transform_data():
    df = pd.DataFrame({"id": [1, 2], "name": ["John", "Alice"], "age": [30, None]})
    transformed_df = transform_data(df)

    assert transformed_df.shape == (1, 3)  # La ligne avec `None` est supprimée
