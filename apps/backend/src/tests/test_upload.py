import os
from fastapi.testclient import TestClient
from CVscan.apps.backend.src.main import app

client = TestClient(app)

def test_upload_cv():
    file_path = os.path.join(os.path.dirname(__file__), "dummy_cv.pdf")
    with open(file_path, "rb") as f:
        response = client.post(
            "/api/v1/upload-cv",
            files={"file": ("dummy_cv.pdf", f, "application/pdf")}
        )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data or "status" in data
