from app import ma
from app.models import Session


class SessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Session
        include_fk = True  # This will include foreign keys automatically

    trainer_id = ma.Int(required=True)
    client_id = ma.Int(required=True)
session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)