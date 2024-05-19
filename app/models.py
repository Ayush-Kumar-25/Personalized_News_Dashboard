from app import db  # Import the SQLAlchemy instance from the app module


class User(db.Model):
    """
    Class to represent the User model in the database
    """

    # Primary key field for the User model, which uniquely identifies each user
    id = db.Column(db.Integer, primary_key=True)

    # Column to store the username of the user
    # - db.String(150): The maximum length of the username is 150 characters
    # - unique=True: Ensures that no two users can have the same username
    # - nullable=False: The username field cannot be empty (it is a required field)
    username = db.Column(db.String(150), unique=True, nullable=False)

    # Column to store the password of the user
    # - db.String(150): The maximum length of the password is 150 characters
    # - nullable=False: The password field cannot be empty (it is a required field)
    password = db.Column(db.String(150), nullable=False)
