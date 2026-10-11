"""
Veritas SQLite Database Setup & Models
Manages metadata, experiment logging, causal graphs, and reproducibility tracking.
"""
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "veritas.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class DatasetModel(Base):
    __tablename__ = "datasets"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    modality = Column(String, default="tabular")
    row_count = Column(Integer, default=0)
    col_count = Column(Integer, default=0)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    profile_data = Column(Text, default="{}")
    causal_graph = Column(Text, default="{}")

    generation_jobs = relationship("GenerationJobModel", back_populates="dataset", cascade="all, delete-orphan")


class GenerationJobModel(Base):
    __tablename__ = "generation_jobs"

    id = Column(String, primary_key=True, index=True)
    dataset_id = Column(String, ForeignKey("datasets.id"))
    model_name = Column(String, nullable=False)
    display_name = Column(String, nullable=False)
    status = Column(String, default="completed")
    num_samples = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)
    output_path = Column(String, nullable=True)
    metrics_json = Column(Text, default="{}")
    shap_json = Column(Text, default="{}")

    dataset = relationship("DatasetModel", back_populates="generation_jobs")


class TextJobModel(Base):
    __tablename__ = "text_jobs"

    id = Column(String, primary_key=True, index=True)
    model_name = Column(String, nullable=False)
    sample_count = Column(Integer, default=5)
    bias_category = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    prompt_used = Column(Text, default="")
    results_json = Column(Text, default="[]")
    evaluation_json = Column(Text, default="{}")


class SettingModel(Base):
    __tablename__ = "settings"

    key = Column(String, primary_key=True, index=True)
    value = Column(String, nullable=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
