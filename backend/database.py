from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database File Name
# Using a hidden file to prevent Live Server from auto-reloading when the DB updates
DATABASE_URL = "sqlite:///./.mediamind.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- TABLE MODEL ---
class ActivityLog(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    feature = Column(String)  # e.g., sentiment, recommend, etc.
    input_text = Column(String)
    output_result = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create Tables
def init_db():
    Base.metadata.create_all(bind=engine)