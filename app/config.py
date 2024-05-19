import os  # Import the os module to interact with the operating system's environment variables

class Config:
    """
    Class to store the configurations of the Flask app
    """

    # Secret key for Flask application, used for session management and other security purposes
    # If the environment variable "SECRET_KEY" is not set, it defaults to "your_secret_key"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key"

    # Database URI for SQLAlchemy, which tells SQLAlchemy what database to connect to
    # If the environment variable "DATABASE_URL" is not set, it defaults to a local SQLite database "users.db"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///users.db"

    # Disables the modification tracking system of SQLAlchemy, which is unnecessary and can add overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key for JWT (JSON Web Tokens), used to sign the tokens
    # If the environment variable "JWT_SECRET_KEY" is not set, it defaults to "your_jwt_secret_key"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "your_jwt_secret_key"
