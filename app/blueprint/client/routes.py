from flask import jsonify, request
from app import app, db
from marshmallow import ValidationError
from app.models import Client  
from app.blueprint.client.schemas import client_schema 
from sqlalchemy import select

#* Client Endpoints
# Create Client Endpoint
@app.route("/api/clients", methods=["POST"])
def create_client():
    try:
        client_data = client_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_client = Client(
        name=client_data['name'],
        email=client_data['email'],
        phone=client_data['phone'],
        dob=client_data['dob'],
        trainer_id=client_data.get('trainer_id')
    )

    db.session.add(new_client)
    db.session.commit()

    return client_schema.jsonify(new_client), 201 

# Retrieve all Clients
@app.route("/api/clients", methods=["GET"])
def get_clients():
    query = select(Client)
    result = db.session.execute(query).scalars().all()
    return client_schema.jsonify(result), 200

# Retrieve Client by ID
@app.route("/api/clients/<int:client_id>", methods=["GET"])
def get_client(client_id):
    query = select(Client).where(Client.id == client_id)
    client = db.session.execute(query).scalars().first()

    if client == None:
        return jsonify({"message": "invalid client id"}), 400

    return client_schema.jsonify(client), 200

# Update Client by ID
@app.route("/api/clients/<int:client_id>", methods=["PUT"])
def update_client(client_id):
    query = select(Client).where(Client.id == client_id)
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