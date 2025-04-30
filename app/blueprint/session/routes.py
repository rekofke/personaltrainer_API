from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError, Schema, fields
from sqlalchemy import select
from app import app, db
from app.models import Session
from app.blueprint.session.schemas import session_schema, sessions_schema
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

#* Session Endpoints
# Create Session Endpoint
@app.route("/api/sessions", methods=["POST"])
def create_session():
    try:
        session_data = session_schema.load(request.json)

        # Ensure required keys exist
        if 'trainer_id' not in session_data or 'client_id' not in session_data:
            return jsonify({"error": "trainer_id and client_id are required."}), 400

        new_session = Session(
            date=session_data['date'],
            type=session_data['type'],
            status=session_data['status'],
            trainer_id=session_data['trainer_id'],
            client_id=session_data['client_id']
        )

        db.session.add(new_session)
        db.session.commit()

        return session_schema.jsonify(new_session), 201

    except ValidationError as e:
        return jsonify(e.messages), 400
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400


    except ValidationError as e:
        return jsonify(e.messages), 400
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
# Retrieve all Sessions
@app.route("/api/sessions", methods=["GET"])
def get_sessions():
    query = select(Session)
    result = db.session.execute(query).scalars().all()
    return sessions_schema.jsonify(result), 200

# Retrieve Session by ID
@app.route("/api/sessions/<int:session_id>", methods=["GET"])
def get_session(session_id):
    query = select(Session).where(Session.id == session_id)
    session = db.session.execute(query).scalars().first()

    if session == None:
        return jsonify({"message": "invalid session id"}), 400

    return session_schema.jsonify(session), 200

# Update Session by ID
@app.route("/api/sessions/<int:session_id>", methods=["PUT"])
def update_sesion(session_id):
    query = select(Session).where(Session.id == session_id)
    session = db.sessions.execute(query).scalars(). first()

    if session == None:
        return jsonify({"message": "invalid session id"}), 400

    try:
        session_data = session_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in session_data.items():
        setattr(session, field, value)

    db.session.commit()
    return session_schema.jsonify(session), 200

# Delete Session by ID
@app.route("/api/sessions/<int:session_id>", methods=["DELETE"])
def delete_session(session_id):
    query = select(Session).where(Session.id == session_id)
    session = db.session.execute(query).scalars().first()

    db.session.delete(session)
    db.session.commit()
    return jsonify({"message": f'sucessfully deleted session {session_id}'}), 200

with app.app_context():
    # db.drop_all()
    db.create_all()