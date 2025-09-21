from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from . import auth, crud, models, schemas
from .database import SessionLocal, engine, get_db, init_db
from utils.analysis_chain import create_analysis_chain

init_db()

app = FastAPI()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Core Application Endpoints ---
@app.post("/reflections/", response_model=schemas.Analysis)
def analyze_reflection(reflection: schemas.ReflectionCreate, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    db_reflection = crud.create_reflection(db=db, reflection=reflection, owner_id=current_user.id)
    
    biases = crud.get_all_biases(db)
    bias_context = "\n".join([f"- **{b.name}**: {b.description}" for b in biases])

    chain = create_analysis_chain()
    analysis_content = chain.invoke({
        "bias_context": bias_context,
        "user_text": reflection.content
    })
    
    db_analysis = crud.create_analysis(db=db, analysis_content=analysis_content, reflection_id=db_reflection.id)
    
    return db_analysis

@app.get("/reflections/", response_model=list[schemas.Reflection])
def get_user_reflections(current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return crud.get_reflections_by_owner(db=db, owner_id=current_user.id)