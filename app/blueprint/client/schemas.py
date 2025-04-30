from app.models import Client 
from app import ma  # Import 'ma' from the app module

class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        include_fk = True  

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)