from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io

app = FastAPI()

@app.get("")
async def hello_world():
    return {"message": "Hello World"}

@app.post("/upload/csv/")
async def upload_csv(file: UploadFile = File(...)):
    df = pd.read_csv(io.BytesIO(await file.read()))
    transformed_df = transform_data(df)
    load_data(transformed_df, "my_table")
    return {"message": "File uploaded and processed successfully"}
