from flask import Flask
from app import create_app, db

# Create the Flask application using the factory function
app: Flask = create_app()

if __name__ == "__main__":
    # Run the application
    with app.app_context():
        """
        Create all database tables within the application context.
        This ensures that the tables are created in the context of the current Flask application.
        """
        db.create_all()
    # Start the Flask application in debug mode
    app.run(debug=True)
