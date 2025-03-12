from fastapi.testclient import TestClient
from api.main import app  # Assurez-vous que `main.py` contient `app = FastAPI()`

client = TestClient(app)

def test_upload_csv():
    file_content = "id,name,age\n1,John,30\n2,Alice,25"
    files = {"file": ("test.csv", file_content, "text/csv")}
    response = client.post("/upload/csv/", files=files)

    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded and processed successfully"}

def test_upload_invalid_file():
    response = client.post("/upload/csv/", files={"file": ("test.txt", "invalid content", "text/plain")})
    
    assert response.status_code == 400
