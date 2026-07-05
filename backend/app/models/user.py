from sqlalchemy import Column, Integer, String, DateTime,Boolean
from datetime import datetime
from app.db.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)

    phone_no = Column(String, nullable=False)

    hashed_password = Column(

        String,

        nullable=False

    )

    role = Column(

        String,
        default="customer",

        nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    is_first_login = Column(
        Boolean,
        default=True,
        nullable=False
    )
    is_verified=Column(
        Boolean,
        default=False,
        nullable=False
    )
    tokens = relationship(
    "UserToken",
    back_populates="user",
    cascade="all, delete-orphan"
)