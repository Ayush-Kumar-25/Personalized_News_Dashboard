from flask import Flask  # Import Flask class to create the app
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for database interactions
from flask_bcrypt import Bcrypt  # Import Bcrypt for password hashing
from flask_jwt_extended import JWTManager  # Import JWTManager for JWT token handling
from app.config import Config  # Import Config class for application configurations
from flask_cors import CORS  # Import CORS to handle Cross-Origin Resource Sharing

# Instantiate extensions
db: SQLAlchemy = SQLAlchemy()  # Initialize SQLAlchemy object for database interactions
bcrypt: Bcrypt = Bcrypt()  # Initialize Bcrypt object for password hashing
jwt: JWTManager = JWTManager()  # Initialize JWTManager object for handling JWT tokens

def create_app() -> Flask:
    """
    Function to create the Flask app with the required configurations.

    Returns:
        Flask: The Flask app instance.
    """
    app: Flask = Flask(__name__)  # Create the Flask app instance
    CORS(app)  # Enable Cross-Origin Resource Sharing for the app
    app.config.from_object(Config)  # Load configurations from Config class

    db.init_app(app)  # Initialize the app with SQLAlchemy
    bcrypt.init_app(app)  # Initialize the app with Bcrypt
    jwt.init_app(app)  # Initialize the app with JWTManager

    from app.routes import auth_blueprint, news_blueprint  # Import blueprints for routes

    # Register blueprints for authentication and news routes
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(news_blueprint)
    
    return app  # Return the app instance
