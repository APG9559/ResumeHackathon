from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    jwt.init_app(app)
    
    # Configure CORS to allow requests from React frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    from .routes import auth, resumes, jobs, evaluation
    app.register_blueprint(auth.bp)
    app.register_blueprint(resumes.bp)
    app.register_blueprint(jobs.bp)
    app.register_blueprint(evaluation.bp)
    
    with app.app_context():
        db.create_all()
    
    return app
