from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Importa e registra os blueprints
    from .front import front_blueprint
    app.register_blueprint(front_blueprint)

    return app
