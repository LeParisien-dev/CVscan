import os
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from CVscan.apps.backend.src.main import app
from db.database import SessionLocal
from db import models

client = TestClient(app)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_upload_cv_inserts_into_db(tmp_path: Path):
    # Prepare a fake TXT CV file
    cv_file_path = tmp_path / "test_cv.txt"
    cv_file_path.write_text("This is a dummy CV content for testing.")

    # Send request to upload endpoint
    with open(cv_file_path, "rb") as f:
        response = client.post(
            "/api/v1/upload-cv",
            files={"file": ("test_cv.txt", f, "text/plain")}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["filename"] == "test_cv.txt"

    # Verify DB insertion
    db: Session = next(get_db())
    doc = db.query(models.CvDocument).filter_by(filename="test_cv.txt").first()

    assert doc is not None
    assert "dummy CV content" in doc.content
    assert isinstance(doc.score, (int, float))
