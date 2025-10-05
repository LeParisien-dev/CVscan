# Description: Lightweight statistical matching (no LLM, no paid deps)
# Notes:
# - Extracts text from CV (local uploads/ or public Supabase URL) and job JSON (jobs/<job_id>.json)
# - Cleans + tokenizes FR/EN
# - Scores with shared keyword ratio -> returns 0.60..0.95

from __future__ import annotations

import os
import io
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Optional PDF libs (already in project according to constraints)
try:
    import pdfplumber  # preferred
except Exception:
    pdfplumber = None

try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None

# Project-relative default dirs (keep consistent with existing code)
UPLOAD_DIR = Path("uploads")
JOBS_DIR = Path("jobs")

# Environment for public Supabase read (no secret required)
SUPABASE_URL = os.getenv("SUPABASE_URL")  # e.g., https://xyzcompany.supabase.co
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "cvscan-files")  # bucket name (public)

# Minimal FR/EN stopwords (short list – pragmatic and robust)
_STOPWORDS: Set[str] = {
    # EN
    "the","a","an","and","or","for","to","of","in","on","with","at","by","from","as",
    "this","that","these","those","is","are","was","were","be","been","being","it",
    "its","you","your","we","our","they","their","i","me","my","he","she","his","her",
    "them","us","but","if","so","not","no","yes","can","could","would","should",
    # FR
    "le","la","les","un","une","des","de","du","au","aux","en","dans","sur","sous","par",
    "pour","avec","sans","chez","ce","cet","cette","ces","et","ou","mais","donc",
    "or","ni","car","est","sont","été","etre","être","avoir","ai","as","a","ont","sera",
    "seront","était","étaient","il","elle","ils","elles","nous","vous","tu","te","ton",
    "ta","tes","mon","ma","mes","nos","vos","leur","leurs","qui","que","quoi","dont",
    "où","deux","trois"
}

_WORD_RE = re.compile(r"[a-z0-9]+", flags=re.IGNORECASE)


# ---------- Public helpers ----------

def load_job_text(job_id: str) -> str:
    """
    Load job description text from jobs/<job_id>.json
    Accepted keys: "description", "text", "content".
    Fallback: stringify JSON.
    """
    path = JOBS_DIR / f"{job_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Job file not found: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise RuntimeError(f"Invalid job JSON: {path}: {e}")
    for key in ("description", "text", "content"):
        if isinstance(data, dict) and key in data and isinstance(data[key], str) and data[key].strip():
            return data[key]
    return json.dumps(data, ensure_ascii=False)


def extract_cv_text(cv_filename: str) -> str:
    """
    Extract CV text from:
    1) Local uploads/<cv_filename> if exists
    2) Else public Supabase URL (no auth), built as:
       {SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{cv_filename}
    Supported types: .pdf (via pdfplumber or PyPDF2), .txt/.md/.json (plain text)
    """
    local_path = UPLOAD_DIR / cv_filename
    if local_path.exists():
        return _extract_from_local_file(local_path)

    # Try public Supabase (no secret key required)
    if not SUPABASE_URL:
        raise FileNotFoundError(
            f"CV not found locally and SUPABASE_URL is not set. Tried: {local_path}"
        )
    public_url = _build_supabase_public_url(cv_filename)
    content, filename = _fetch_bytes(public_url, fallback_name=cv_filename)

    if filename.lower().endswith(".pdf") or cv_filename.lower().endswith(".pdf"):
        return _extract_from_pdf_bytes(content)
    elif filename.lower().endswith((".txt", ".md", ".json")) or cv_filename.lower().endswith((".txt", ".md", ".json")):
        try:
            return content.decode("utf-8", errors="ignore")
        except Exception:
            return content.decode("latin-1", errors="ignore")
    else:
        # Best-effort: try as text
        try:
            return content.decode("utf-8", errors="ignore")
        except Exception:
            return content.decode("latin-1", errors="ignore")


def compute_match_score(cv_text: str, job_text: str, top_n: int = 15) -> Dict:
    """
    Clean + tokenize both texts, compute common words and ratio, then map to [0.60, 0.95].
    Returns dict with score and details.
    """
    cv_tokens = tokenize(cv_text)
    job_tokens = tokenize(job_text)

    set_cv = set(cv_tokens)
    set_job = set(job_tokens)

    common = set_cv.intersection(set_job)
    n_common = len(common)
    n_job = len(set_job)
    n_cv = len(set_cv)

    ratio = n_common / max(1, n_job)
    raw_score = 0.60 + 0.35 * ratio
    score = max(0.60, min(0.95, raw_score))

    # Rank top common by frequency in CV + Job
    freq_cv = _freq(cv_tokens)
    freq_job = _freq(job_tokens)
    scored_common = []
    for w in common:
        scored_common.append((w, freq_cv.get(w, 0) + freq_job.get(w, 0)))
    scored_common.sort(key=lambda t: t[1], reverse=True)
    top_common = [w for (w, _) in scored_common[:top_n]]

    return {
        "score": round(score, 4),
        "details": {
            "n_common": n_common,
            "n_job_tokens": n_job,
            "n_cv_tokens": n_cv,
            "ratio_job_to_cv": round(ratio, 4),
            "top_common": top_common
        }
    }


def match_stat(cv_filename: str, job_id: str) -> Dict:
    """
    Orchestrate the full pipeline: load texts, then compute score.
    """
    cv_text = extract_cv_text(cv_filename)
    job_text = load_job_text(job_id)
    return compute_match_score(cv_text, job_text)


# ---------- Internal utilities ----------

def _build_supabase_public_url(cv_filename: str) -> str:
    """
    Build public object URL for Supabase Storage.
    Pattern: {SUPABASE_URL}/storage/v1/object/public/{bucket}/{path}
    """
    base = SUPABASE_URL.rstrip("/")
    bucket = SUPABASE_BUCKET.strip("/")
    path = cv_filename.lstrip("/")
    return f"{base}/storage/v1/object/public/{bucket}/{path}"


def _fetch_bytes(url: str, fallback_name: Optional[str] = None) -> Tuple[bytes, str]:
    """
    Fetch bytes from URL, return (content, filename_guess).
    Uses only stdlib (urllib).
    """
    headers = {
        "User-Agent": "CVScan-MatchStat/1.0"
    }
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=20) as resp:
            content = resp.read()
            # filename hint from URL (best-effort)
            filename = fallback_name or url.split("?")[0].split("/")[-1] or "file"
            return content, filename
    except HTTPError as e:
        raise FileNotFoundError(f"HTTP error fetching CV: {url} -> {e.code}") from e
    except URLError as e:
        raise ConnectionError(f"Network error fetching CV: {url} -> {e}") from e


def _extract_from_local_file(path: Path) -> str:
    """
    Extract text from local file path.
    """
    name = path.name.lower()
    if name.endswith(".pdf"):
        return _extract_from_pdf_path(path)
    elif name.endswith((".txt", ".md", ".json")):
        return path.read_text(encoding="utf-8", errors="ignore")
    else:
        # Best-effort as text
        return path.read_text(encoding="utf-8", errors="ignore")


def _extract_from_pdf_path(path: Path) -> str:
    """
    Extract text from local PDF using pdfplumber or PyPDF2.
    """
    if pdfplumber:
        try:
            text_parts: List[str] = []
            with pdfplumber.open(str(path)) as pdf:
                for page in pdf.pages:
                    txt = page.extract_text() or ""
                    text_parts.append(txt)
            return "\n".join(text_parts)
        except Exception:
            pass
    if PdfReader:
        try:
            reader = PdfReader(str(path))
            parts = []
            for page in reader.pages:
                parts.append(page.extract_text() or "")
            return "\n".join(parts)
        except Exception:
            pass
    # Fallback
    return ""


def _extract_from_pdf_bytes(content: bytes) -> str:
    """
    Extract text from PDF bytes using pdfplumber or PyPDF2.
    """
    if pdfplumber:
        try:
            text_parts: List[str] = []
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                for page in pdf.pages:
                    txt = page.extract_text() or ""
                    text_parts.append(txt)
            return "\n".join(text_parts)
        except Exception:
            pass
    if PdfReader:
        try:
            reader = PdfReader(io.BytesIO(content))
            parts = []
            for page in reader.pages:
                parts.append(page.extract_text() or "")
            return "\n".join(parts)
        except Exception:
            pass
    # Fallback
    return ""


def clean(text: str) -> str:
    """
    Lowercase + keep alphanumerics + collapse spaces.
    """
    text = text.lower()
    tokens = _WORD_RE.findall(text)
    return " ".join(tokens)


def tokenize(text: str) -> List[str]:
    """
    Clean + split + remove stopwords + length >= 2.
    """
    cleaned = clean(text)
    tokens = [t for t in cleaned.split() if len(t) >= 2 and t not in _STOPWORDS]
    return tokens


def _freq(tokens: List[str]) -> Dict[str, int]:
    """
    Simple frequency counter.
    """
    out: Dict[str, int] = {}
    for t in tokens:
        out[t] = out.get(t, 0) + 1
    return out
