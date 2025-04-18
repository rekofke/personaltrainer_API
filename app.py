from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Date, Table, Column
from typing import List, Optional

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:C%40ntget1n@localhost/module_project'

db.init_app(app)

# Association table for many-to-many relationship between trainers and sessions
trainer_session = db.Table(
    'trainer_session',
    Base.metadata,
    db.Column('trainer_id', ForeignKey('trainers.id')),
    db.Column('session_id', ForeignKey('sessions.id')),
)


# trainer_session = Table(
#     'trainer_session',
#     Base.metadata,
#     Column('trainer_id', Integer, ForeignKey('trainers.id'), primary_key=True),
#     Column('session_id', Integer, ForeignKey('sessions.id'), primary_key=True)
#)


class Trainer(Base):
    __tablename__ = 'trainers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    phone: Mapped[str] = mapped_column(String(150))

    # One trainer can have many clients
    clients: Mapped[List['Client']] = relationship(back_populates='trainer')
    # One trainer can conduct many sessions
    sessions: Mapped[List['Session']] = relationship(back_populates='trainer')
    sessions: Mapped[List['Session']] = relationship(secondary=trainer_session)

class Client(Base): 
    __tablename__ = 'clients'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    phone: Mapped[str] = mapped_column(String(150))
    dob: Mapped[Date] = mapped_column(Date)  # Changed from String to Date
    trainer_id: Mapped[Optional[int]] = mapped_column(ForeignKey('trainers.id'), nullable=True)

    # Many clients can have one trainer
    trainer: Mapped[Optional['Trainer']] = relationship(back_populates='clients')
    # One client can have many sessions
    sessions: Mapped[List['Session']] = relationship(back_populates='client')
    


class Session(Base):
    __tablename__ = 'sessions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_date: Mapped[Date] = mapped_column(Date)
    session_type: Mapped[str] = mapped_column(String(150))
    status: Mapped[str] = mapped_column(String(150))
    trainer_id: Mapped[int] = mapped_column(ForeignKey('trainers.id'))
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))

    # Many sessions belong to one trainer
    trainer: Mapped['Trainer'] = relationship(back_populates='sessions')
    # Many sessions belong to one client
    client: Mapped['Client'] = relationship(back_populates='sessions')
    trainers: Mapped[List["Trainer"]] = db.relationship(secondary=trainer_session)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)