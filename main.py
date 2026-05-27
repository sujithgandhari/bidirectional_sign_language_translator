"""
Bidirectional Sign Language Translator — FastAPI Backend
Run:  uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, predict, tts

app = FastAPI(title="Sign Language Translator API", version="1.0.0")

# Allow your frontend (served on any port) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # change to ["http://localhost:5500"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register routers ──────────────────────────────────────────────
app.include_router(auth.router,    prefix="/auth",    tags=["Auth"])
app.include_router(predict.router, prefix="/predict", tags=["Prediction"])
app.include_router(tts.router,     prefix="/tts",     tags=["Text-to-Sign"])

@app.get("/")
def root():
    return {"message": "Sign Language Translator API is running ✅"}
