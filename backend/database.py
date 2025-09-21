from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
from . import models

DATABASE_URL = "sqlite:///./reflections.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Seed the database with cognitive biases
    db = SessionLocal()
    try:
        # Check if the table is already seeded
        if db.query(models.CognitiveBias).count() == 0:
            print("Seeding database with cognitive biases...")
            biases_df = pd.read_csv("data/biases.csv")
            # FIX: Changed column access to lowercase to match the CSV file
            for _, row in biases_df.iterrows():
                db_bias = models.CognitiveBias(name=row["name"], description=row["description"])
                db.add(db_bias)
            db.commit()
            print("Seeding complete.")
        else:
            print("Cognitive biases already exist in the database.")
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()