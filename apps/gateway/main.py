from fastapi import FastAPI

app = FastAPI()

@app.get("/api/health")
def health_check():
    return {"message": "API is running!"}
