from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError, Schema, fields
from sqlalchemy import select
from app import app, db
from app.models import Trainer
from app.blueprint.trainer.schemas import trainer_schema, trainers_schema
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

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
    return trainer_schema.jsonify(result), 200

# Retrieve Trainer by ID
@app.route("/api/trainers/<int:trainer_id>", methods=["GET"])
def get_trainer(trainer_id):
    query = select(Trainer).where(Trainer.id == trainer_id)
    trainer = db.session.execute(query).scalars().first()

    if trainer is None:
        return jsonify({"message": "invalid trainer id"}), 400

    return trainer_schema.jsonify(trainer), 200

# Update Trainer by ID
@app.route("/api/trainers/<int:trainer_id>", methods=["PUT"])
def update_trainer(trainer_id):
    query = select(Trainer).where(Trainer.id == trainer_id)
    trainer = db.session.execute(query).scalars().first()

    if trainer is None:
        return jsonify({"message": "invalid trainer id"}), 400

    try:
        trainer_data = trainer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in trainer_data.items():
        setattr(trainer, field, value)

    db.session.commit()
    return trainer_schema.jsonify(trainer), 200

# Delete Trainer by ID
@app.route("/api/trainers/<int:trainer_id>", methods=["DELETE"])
def delete_trainer(trainer_id):
    query = select(Trainer).where(Trainer.id == trainer_id)
    trainer = db.session.execute(query).scalars().first()
    if trainer is None:
        return jsonify({"message": "invalid trainer id"}), 400
    db.session.delete(trainer)
    db.session.commit()
    return jsonify({"message": f'sucessfully deleted trainer {trainer_id}'}), 200