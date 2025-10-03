from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import shutil
from pathlib import Path
from sqlalchemy.orm import Session

from src.utils.parsers import extract_text_from_pdf
from src.utils.scoring import score_text
from src.core.database import SessionLocal
from src.models.cv_document import CVDocument

router = APIRouter()

# Directory for storing uploaded files
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint: upload a CV
@router.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Validate file type
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF or TXT files are allowed")

    file_path = UPLOAD_DIR / file.filename

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text depending on file type
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(str(file_path))
    else:  # TXT file
        try:
            text = file_path.read_text(encoding="utf-8")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading TXT: {e}")

    # Compute score
    score = score_text(text)

    # Insert document into the database
    cv_doc = CvDocument(
        filename=file.filename,
        content=text,
        score=score
    )
    db.add(cv_doc)
    db.commit()
    db.refresh(cv_doc)

    # Return response
    return {
        "status": "success",
        "filename": file.filename,
        "score": score,
        "id": cv_doc.id,
        "message": "CV uploaded, processed, and stored successfully"
    }
