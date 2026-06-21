from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime
from app.db.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    premium = Column(Float, nullable=False)

    risk_score = Column(Integer, nullable=False)

    risk_level = Column(String, nullable=False)

    validity_years = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)