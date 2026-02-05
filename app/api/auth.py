# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.core.deps import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.auth import UserCreate, Token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get('/')
def hi():
    return {"message" : "welcome to the authetication page"}

@router.post("/signup", status_code=201)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(
        (User.username == user_in.username) |
        (User.email == user_in.email)
    ).first():
        raise HTTPException(400, "User already exists")

    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hash_password(user_in.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"msg": "User created"}

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.id})
    return {"access_token": token}
