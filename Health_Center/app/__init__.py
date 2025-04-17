from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os 


db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-key"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_center.db'
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.routes.auth_routes import auth_routes
    app.register_blueprint(auth_routes)

    
    return app