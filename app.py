from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Date, Table, Column, select
from typing import List, Optional

class Base(DeclarativeBase):
    pass

# create the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:C%40ntget1n@127.0.0.1/module_project'
db = SQLAlchemy(model_class=Base)
ma = Marshmallow(app)

db.init_app(app)

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
    session_date: Mapped[Date] = mapped_column(Date)
    session_type: Mapped[str] = mapped_column(String(150))
    status: Mapped[str] = mapped_column(String(150))
    trainer_id: Mapped[int] = mapped_column(ForeignKey('trainers.id'))
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))

    # Many sessions belong to one client
    client: Mapped['Client'] = relationship(back_populates='sessions')
    # Many-to-many relationship with trainers
    trainers: Mapped[List["Trainer"]] = relationship(secondary=trainer_session, back_populates='sessions', overlaps="sessions")


#* Schemas
    
class TrainerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trainer

trainer_schema = TrainerSchema()
trainers_schema = TrainerSchema(many=True)

class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Client
client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)

class SessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Session
session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)

#* Routes/Endpoints
# Create Trainer Endpoint
@app.route("/api/trainers", methods=["POST"])
def create_trainer():
    try:
        trainer_data = trainer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_trainer = Trainer(name=trainer_data['name'], email=trainer_data['email'], phone=trainer_data['phone'])

    #Save new_trainer to DB
    db.session.add(new_trainer)
    db.session.commit()

    return trainer_schema.jsonify(new_trainer), 201

# Retrieve all Trainers
@app.route("/api/trainers", methods=["GET"])
def get_trainers():
    query = select(Trainer)
    result = db.session.execute(query).scalars().all()
    return trainers_schema.jsonify(result), 200

# Retrieve Trainer by ID
@app.route("/api/trainers/<int:trainer_id>", methods=["GET"])
def get_trainer(trainer_id):
    query = select(Trainer).where(Trainer.id == trainer_id)
    trainer = db.session.execute(query).scalars().first()

    if trainer is None:
        return jsonify({"message": "invalid trainer id"}), 400

    return trainer_schema.jsonify(trainer), 200

#* Client Endpoints
# Create Client Endpoint
@app.route("/api/clients", methods=["POST"])
def create_client():
    try:
        client_data = client_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_client = Client(name=client_data['name'], email=client_data['email'], phone=client_data['phone'], dob=client_data['dob'], trainer_id=client_data.get('trainer_id'))

    db.session.add(new_client)
    db.session.commit()

# Retrieve all Clients
@app.route("/api/clients", methods=["GET"])
def get_clients():
    query = select(Client)
    result = db.session.execute(query).scalalars().all()
    return clients_schema.jsonify(result), 200

# Retrieve Client by ID
@app.route("/api/clients/<int:client_id>", method=["GET"])
def get_client(client_id):
    query = select(Client).where(Client.id == client_id)
    client = db.session.execute(query).scalars().first()

    if client == None:
        return jsonify({"message": "invalid client id"}), 400

    return clients_schema.jsonify(client), 200

# Update Client by ID
@app.route("/api/clients/<int:client_id>", methods=["PUT"])
def update_client(client_id):
    query = select(Cliebnt).where(Client.id == client_id)
    client = db.session.execute(query).scalars(). first()

    if client == None:
        return jsonify({"message": "invalid client id"}), 400

    try:
        client_data = client_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in client_data.items():
        setattr(client, field, value)

    db.session.commit()
    return client_schema.jsonify(client), 200

# Delete Client by ID
@app.route("/api/clients/<int:client_id>", methods=["DELETE"])
def delete_client(client_id):
    query = select(Client).where(Client.id == client_id)
    client = db.session.execute(query).scalars().first()

    db.session.delete(client)
    db.session.commit()
    return jsonify({"message": f'sucessfully deleted client {client_id}'}), 200
#* Session Endpoints
# Create Session Endpoint


# Retrieve all Sessions


# Retrieve Session by ID


# Update Session by ID


# Delete Session by ID


with app.app_context():
    db.create_all()
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)