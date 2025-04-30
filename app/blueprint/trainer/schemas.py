from app import ma
from app.models import Trainer


class TrainerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trainer

trainer_schema = TrainerSchema()
trainers_schema = TrainerSchema(many=True)