"""
/tts/text_to_sign — accepts a sentence, returns a list of sign
image filenames (one per letter/word) to render in the browser.

Phase 1: letter-by-letter lookup from a local static folder.
Phase 2 (future): swap lookup() for your gesture animation model.
"""

from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

router = APIRouter()

# Folder: backend/static/signs/  — put images like A.png, B.png …
SIGNS_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "signs")

class TextRequest(BaseModel):
    text: str

def lookup(char: str) -> str | None:
    """Return URL path for a sign image, or None if not found."""
    char = char.upper()
    for ext in ("png", "jpg", "gif", "webp"):
        if os.path.isfile(os.path.join(SIGNS_DIR, f"{char}.{ext}")):
            return f"/static/signs/{char}.{ext}"
    return None

@router.post("/text_to_sign")
def text_to_sign(req: TextRequest):
    """Return an ordered list of sign image URLs for each letter."""
    results = []
    for ch in req.text:
        if ch == " ":
            results.append({"char": " ", "image": None, "type": "space"})
        else:
            url = lookup(ch)
            results.append({
                "char": ch,
                "image": url,
                "type": "sign" if url else "unknown"
            })
    return {"signs": results}
