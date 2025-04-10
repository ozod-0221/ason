from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
import datetime
from sqlalchemy import Column, BigInteger, String, Enum as SQLAEnum
Base = declarative_base()
import enum

from sqlalchemy import Enum
from datetime import datetime

class RoleEnum(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

class User(Base):
    __tablename__ = "users"

    telegram_user_id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)

    role = Column(SQLAEnum(RoleEnum), default=RoleEnum.USER)
    events = relationship("EventParticipant", back_populates="user")
    



class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    events_referal_id = Column(String, unique=True, nullable=False)
    
    is_active = Column(Boolean, default=False)
    link = Column(String, nullable=False)
    participants = relationship("EventParticipant", back_populates="event")
class EventParticipant(Base):
    __tablename__ = 'event_participants'

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)  # events.id ga bog'langan
    telegram_user_id = Column(BigInteger, ForeignKey('users.telegram_user_id'), nullable=False)
    joined_at = Column(DateTime, nullable=False, default=datetime.now)  # default qiymat qo'shildi

    event = relationship("Event", back_populates="participants")
    user = relationship("User", back_populates="events")

    