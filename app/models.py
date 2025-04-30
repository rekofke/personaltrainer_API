from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from typing import List, Optional

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


# Association table for many-to-many relationship between trainers and sessions
trainer_session = Table(
    'trainer_session',
    Base.metadata,
    Column('trainer_id', Integer, ForeignKey('trainers.id'), primary_key=True),
    Column('session_id', Integer, ForeignKey('sessions.id'), primary_key=True)
)


class Trainer(Base):
    __tablename__ = 'trainers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    phone: Mapped[str] = mapped_column(String(150))

    # One trainer can have many clients
    clients: Mapped[List['Client']] = relationship(back_populates='trainer')
    # Many-to-many relationship with sessions
    sessions: Mapped[List['Session']] = relationship(secondary=trainer_session, back_populates='trainers')


class Client(Base): 
    __tablename__ = 'clients'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    phone: Mapped[str] = mapped_column(String(150))
    dob: Mapped[Date] = mapped_column(Date)
    trainer_id: Mapped[Optional[int]] = mapped_column(ForeignKey('trainers.id'), nullable=True)

    # Many clients can have one trainer
    trainer: Mapped[Optional['Trainer']] = relationship(back_populates='clients')
    # One client can have many sessions
    sessions: Mapped[List['Session']] = relationship(back_populates='client')
    
class Session(Base):
    __tablename__ = 'sessions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[Date] = mapped_column(Date)
    type: Mapped[str] = mapped_column(String(150))
    status: Mapped[str] = mapped_column(String(150))
    trainer_id: Mapped[int] = mapped_column(ForeignKey('trainers.id'))
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))

    # Many sessions belong to one client
    client: Mapped['Client'] = relationship(back_populates='sessions')
    # Many-to-many relationship with trainers
    trainers: Mapped[List["Trainer"]] = relationship(secondary=trainer_session, back_populates='sessions', overlaps="sessions")
