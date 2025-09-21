from sqlalchemy.orm import Session
from . import models, schemas
from .utils import get_password_hash

# --- User CRUD ---
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    # This function is now corrected and robust
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Reflection CRUD ---
def create_reflection(db: Session, reflection: schemas.ReflectionCreate, owner_id: int):
    db_reflection = models.Reflection(**reflection.dict(), owner_id=owner_id)
    db.add(db_reflection)
    db.commit()
    db.refresh(db_reflection)
    return db_reflection

def get_reflections_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Reflection).filter(models.Reflection.owner_id == owner_id).offset(skip).limit(limit).all()

# --- Analysis CRUD ---
def create_analysis(db: Session, analysis_content: str, reflection_id: int):
    db_analysis = models.Analysis(content=analysis_content, reflection_id=reflection_id)
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

# --- Cognitive Bias CRUD ---
def get_all_biases(db: Session):
    return db.query(models.CognitiveBias).all()