from sqlalchemy import Column,String,Integer,Float,DateTime,Enum,ForeignKey,func,JSON,Text
from app.db.database import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
class AuditTable(Base):
    __tablename__='audit_log'
    id=Column(Integer,primary_key=True ,index=True)
    

    event = Column(String(100), nullable=False)

    level = Column(String(20), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    email = Column(String(255), nullable=True)

    endpoint = Column(String(255), nullable=False)

    method = Column(String(10), nullable=False)

    status_code = Column(Integer, nullable=False)

    ip_address = Column(String(45), nullable=True)

    message = Column(Text, nullable=True)

    payload = Column(JSONB, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship(
        "User",
        back_populates="audit_log"
    )