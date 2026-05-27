"""
/predict/sign_to_text  — receives a base64 webcam frame,
runs MediaPipe hand landmark extraction → CNN classifier → returns letter.

/predict/sentence      — accepts a sequence of letters,
runs the fake-LLM corrector and returns a clean sentence.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import base64, re, cv2
import numpy as np

router = APIRouter()

# ── Schemas ───────────────────────────────────────────────────────
class FrameRequest(BaseModel):
    image_base64: str   # raw base64, no "data:image/..." prefix

class SentenceRequest(BaseModel):
    raw_text: str

# ── ML pipeline (lazy-loaded so server starts fast) ──────────────
_model = None

def get_model():
    global _model
    if _model is None:
        # Try to import real model; fall back to stub if not ready
        try:
            from ml_models.cnn_rfc import SignClassifier
            _model = SignClassifier()
        except Exception:
            _model = _StubClassifier()
    return _model

class _StubClassifier:
    """Returns random letters — replace with your trained model."""
    import random as _r
    def predict(self, frame: np.ndarray) -> str:
        return self._r.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# ── Text corrector (same logic as your original app.py) ──────────
def llm_correct(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return text
    text = text[0].upper() + text[1:]
    if text[-1] not in ".?!":
        text += "."
    return text

# ── Routes ────────────────────────────────────────────────────────
@router.post("/sign_to_text")
def sign_to_text(req: FrameRequest):
    """Decode base64 frame → run classifier → return predicted letter."""
    try:
        img_bytes = base64.b64decode(req.image_base64)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image data")

    if frame is None:
        raise HTTPException(status_code=400, detail="Could not decode image")

    letter = get_model().predict(frame)
    return {"letter": letter}

@router.post("/sentence")
def build_sentence(req: SentenceRequest):
    """Run LLM-style correction on accumulated text."""
    corrected = llm_correct(req.raw_text)
    return {"original": req.raw_text, "corrected": corrected}
