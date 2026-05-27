"""
Auth routes: /auth/signup  /auth/login  /auth/me
Uses SQLite via SQLAlchemy (swap to PostgreSQL by changing DATABASE_URL).
Passwords hashed with bcrypt. JWT tokens for sessions.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional
import jwt, bcrypt

from database.db import SessionLocal, engine
from database import models as db_models

db_models.Base.metadata.create_all(bind=engine)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = "CHANGE_THIS_IN_PRODUCTION"   # use os.environ["SECRET_KEY"]
ALGORITHM  = "HS256"
TOKEN_EXPIRE_MINUTES = 60 * 24              # 24 hours

# ── Pydantic schemas ──────────────────────────────────────────────
class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ── Helpers ───────────────────────────────────────────────────────
def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# ── Routes ────────────────────────────────────────────────────────
@router.post("/signup", status_code=201)
def signup(req: SignupRequest):
    db = SessionLocal()
    if db.query(db_models.User).filter_by(email=req.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = db_models.User(
        name=req.name,
        email=req.email,
        hashed_password=hash_password(req.password)
    )
    db.add(user)
    db.commit()
    db.close()
    return {"message": "Account created successfully"}

@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = db.query(db_models.User).filter_by(email=form.username).first()
    db.close()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_token({"sub": user.email},
                         timedelta(minutes=TOKEN_EXPIRE_MINUTES))
    return {"access_token": token}

@router.get("/me")
def me(current_user: str = Depends(get_current_user)):
    db = SessionLocal()
    user = db.query(db_models.User).filter_by(email=current_user).first()
    db.close()
    return {"name": user.name, "email": user.email}
