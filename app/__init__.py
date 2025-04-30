from flask import Flask
from .models import db
from .extensions import ma

def create_app(config_name):
    
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    # add extensions to app
    db.init_app(app)
    ma.init_app(app)
    return app