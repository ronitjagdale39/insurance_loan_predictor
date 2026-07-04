from sqlalchemy import Column, Integer, String, Boolean,DateTime,ForeignKey
from datetime import datetime
from app.db.database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id=Column(Integer,primary_key=True,index=True)
    user_id = Column(
    Integer,
    ForeignKey("users.id"),
    nullable=False,
    index=True
    )
    token_hash=Column(String,unique=True,index=True,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)
    expires_at=Column(DateTime,nullable=False)