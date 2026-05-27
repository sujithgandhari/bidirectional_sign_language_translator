# 🤟 Bidirectional Sign Language Translator — Complete Project Guide

---

## 📁 Folder Structure

```
sign_language_project/
│
├── frontend/                   ← Your HTML pages (already built)
│   ├── index.html              ← Main app / workflow page
│   ├── login.html              ← Login page  (now wired to backend)
│   └── signup.html             ← Signup page (now wired to backend)
│
├── backend/                    ← FastAPI server (NEW)
│   ├── main.py                 ← App entry point, registers all routes
│   ├── requirements.txt        ← All Python packages
│   │
│   ├── routes/
│   │   ├── auth.py             ← /auth/signup, /auth/login, /auth/me
│   │   ├── predict.py          ← /predict/sign_to_text, /predict/sentence
│   │   └── tts.py              ← /tts/text_to_sign
│   │
│   ├── database/
│   │   ├── db.py               ← SQLAlchemy engine (SQLite by default)
│   │   └── models.py           ← User table definition
│   │
│   └── static/
│       └── signs/              ← Put A.png, B.png … Z.png here
│
└── ml_models/
    ├── cnn_rfc.py              ← MediaPipe + CNN + RFC classifier
    └── rfc_model.pkl           ← Your trained model (add when ready)
```

---

## 🚀 How to Run — Step by Step

### Step 1 — Install Python (once)
Download Python 3.11+ from https://python.org and install it.
Tick **"Add Python to PATH"** during install.

### Step 2 — Open a terminal in the project folder
```
cd sign_language_project/backend
```

### Step 3 — Create a virtual environment (once)
```bash
python -m venv venv
```

### Step 4 — Activate the virtual environment
**Windows:**
```bash
venv\Scripts\activate
```
**Mac / Linux:**
```bash
source venv/bin/activate
```
You should see `(venv)` in your prompt.

### Step 5 — Install all packages (once)
```bash
pip install -r requirements.txt
```
This installs FastAPI, bcrypt, SQLAlchemy, MediaPipe, PyTorch, etc.

### Step 6 — Start the backend server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 7 — Open the frontend
Open `frontend/login.html` in your browser.
Or use VS Code's **Live Server** extension — right-click the file → "Open with Live Server".

---

## 🔌 API Endpoints

| Method | URL | What it does |
|--------|-----|-------------|
| POST | `/auth/signup` | Create new account |
| POST | `/auth/login` | Login → returns JWT token |
| GET | `/auth/me` | Get logged-in user info |
| POST | `/predict/sign_to_text` | Send webcam frame → get letter |
| POST | `/predict/sentence` | Send raw text → get corrected sentence |
| POST | `/tts/text_to_sign` | Send text → get sign image list |

### Test in browser
Visit http://localhost:8000/docs for the interactive Swagger UI.

---

## 🏗️ Project Phases

### Phase 1 — Auth (DONE ✅)
- Signup / Login working with real database
- Passwords hashed (bcrypt), sessions via JWT token
- Frontend forms wired to backend

### Phase 2 — Sign-to-Text (In Progress 🔧)
- Backend stub returns random letters
- **Your job:** train your CNN+RFC model, save as `rfc_model.pkl`
- Drop `rfc_model.pkl` into `ml_models/`
- Real predictions will start working automatically

### Phase 3 — Text-to-Sign (Planned 📋)
- Add sign images (A.png … Z.png) into `backend/static/signs/`
- The `/tts/text_to_sign` endpoint already serves them
- Wire the frontend to call this endpoint and display images

### Phase 4 — Real-time Webcam (Planned 📋)
- Add webcam capture to `index.html` (use `getUserMedia`)
- Capture frames → send base64 to `/predict/sign_to_text` every ~500ms
- Display returned letters on screen

---

## 🔁 How Frontend Talks to Backend

Login example (already in your login.html):
```javascript
const res = await fetch("http://localhost:8000/auth/login", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({ username: email, password })
});
const { access_token } = await res.json();
localStorage.setItem("token", access_token);
```

Sending a webcam frame:
```javascript
// Capture frame from <video> element to <canvas>
const canvas = document.createElement("canvas");
canvas.width = 256; canvas.height = 256;
canvas.getContext("2d").drawImage(videoElement, 0, 0, 256, 256);
const base64 = canvas.toDataURL("image/jpeg").split(",")[1];

const res = await fetch("http://localhost:8000/predict/sign_to_text", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + localStorage.getItem("token")
  },
  body: JSON.stringify({ image_base64: base64 })
});
const { letter } = await res.json();
```

---

## ⚠️ Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: fastapi` | Run `pip install -r requirements.txt` inside venv |
| `CORS error in browser` | Make sure `--host 0.0.0.0` is in uvicorn command |
| `401 Unauthorized` | Token expired or missing — log in again |
| `No hand detected (?)` | MediaPipe could not find a hand — improve lighting |
| `rfc_model.pkl not found` | Model not trained yet — stub returns random letters |

---

## 📦 Dependencies Summary

| Package | Purpose |
|---------|---------|
| fastapi | Web framework |
| uvicorn | ASGI server to run FastAPI |
| sqlalchemy | Database ORM |
| bcrypt | Password hashing |
| PyJWT | JWT token creation/verification |
| mediapipe | Hand landmark detection |
| opencv-python | Image decode & processing |
| scikit-learn | Random Forest Classifier |
| torch / torchvision | CNN feature extraction |
