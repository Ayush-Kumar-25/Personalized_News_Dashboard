import feedparser
from app import db, bcrypt
from app.models import User
from flask import Blueprint, request, jsonify, Response, render_template, send_from_directory
from app.utils import extract_news_details, calculate_sentiment_score
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from typing import Dict, List, Union, Any, Optional

# Define blueprints for authentication and news routes
auth_blueprint: Blueprint = Blueprint("auth", __name__)
news_blueprint: Blueprint = Blueprint("news", __name__)

@auth_blueprint.route("/", methods=["GET"])
def home() -> Response:
    """
    Serve the index.html page.

    Returns:
        Response: The rendered index.html page.
    """
    return render_template("index.html")

@auth_blueprint.route("/test", methods=["GET"])
def test() -> Response:
    """
    Function to test the API.

    Returns:
        Response: JSON response with a message and HTTP status code 200.
    """
    return jsonify(message="Test successful"), 200

@auth_blueprint.route("/register", methods=["POST"])
def register() -> Response:
    """
    Endpoint to register a new user.

    Expects:
        JSON payload with "username" and "password" fields.

    Returns:
        Response: JSON response with a message and HTTP status code.
    """
    data: Optional[Dict[str, Any]] = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        # Return an error response if username or password is missing
        return jsonify(message="Missing username or password"), 400

    # Hash the password for secure storage
    hashed_password: str = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    # Create a new user instance
    new_user: User = User(username=data["username"], password=hashed_password)
    # Add and commit the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User registered successfully"), 201

@auth_blueprint.route("/login", methods=["POST"])
def login() -> Response:
    """
    Endpoint to log in a user.

    Expects:
        JSON payload with "username" and "password" fields.

    Returns:
        Response: JSON response with an access token and HTTP status code, or an error message.
    """
    data: Optional[Dict[str, Any]] = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        # Return an error response if username or password is missing
        return jsonify(message="Missing username or password"), 400

    # Query the database for the user with the provided username
    user: Optional[User] = User.query.filter_by(username=data["username"]).first()
    # Check if user exists and password matches
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        # Create an access token for the user
        access_token: str = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401

@news_blueprint.route("/news/<string:category>", methods=["GET"])
@jwt_required()
def get_news(category: str) -> Response:
    """
    Endpoint to get news articles based on category.

    Args:
        category (str): The news category to fetch articles for.

    Returns:
        Response: JSON response with the list of news articles and their sentiment scores, or an error message.
    """
    # Dictionary mapping categories to their respective RSS feed URLs
    urls: Dict[str, str] = {
        "india": "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
        "sports": "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms",
        "entertainment": "http://timesofindia.indiatimes.com/rssfeeds/1081479906.cms",
        "science": "https://timesofindia.indiatimes.com/rssfeeds/-2128672765.cms",
        "world": "http://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
        "technology": "http://timesofindia.indiatimes.com/rssfeeds/66949542.cms",
        "top-stories": "http://timesofindia.indiatimes.com/rssfeedstopstories.cms",
        "most-recent": "http://timesofindia.indiatimes.com/rssfeedmostrecent.cms",
        "business": "http://timesofindia.indiatimes.com/rssfeeds/1898055.cms",
        "us": "https://timesofindia.indiatimes.com/rssfeeds_us/72258322.cms",
        "cricket": "http://timesofindia.indiatimes.com/rssfeeds/54829575.cms",
        "life-style": "http://timesofindia.indiatimes.com/rssfeeds/2886704.cms",
        "astrology": "https://timesofindia.indiatimes.com/rssfeeds/65857041.cms",
        "nri": "http://timesofindia.indiatimes.com/rssfeeds/7098551.cms",
        "environment": "http://timesofindia.indiatimes.com/rssfeeds/2647163.cms",
        "education": "http://timesofindia.indiatimes.com/rssfeeds/913168846.cms",
    }
    if category in urls:
        # Parse the RSS feed for the given category
        feed: feedparser.FeedParserDict = feedparser.parse(urls[category])
        # Extract news details from the feed entries
        extracted_news: List[Dict[str, Any]] = extract_news_details(feed.entries)
        # Calculate sentiment score for each news heading
        for news in extracted_news:
            news["sentiment_score"] = calculate_sentiment_score(news["heading"])
        return jsonify(extracted_news), 200
    return jsonify(message="Category not found"), 404

@auth_blueprint.route("/sentimentScore", methods=["POST"])
def sentimentScore() -> Response:
    """
    Endpoint to calculate the sentiment score of a news headline.

    Expects:
        JSON payload with "heading" field.

    Returns:
        Response: JSON response with the sentiment score and HTTP status code.
    """
    data: Optional[Dict[str, Any]] = request.get_json()
    if not data or not data.get("heading"):
        # Return an error response if heading is missing
        return jsonify(message="Missing heading"), 400
    heading: str = data["heading"]
    # Calculate sentiment score for the provided heading
    print(f"Sentiment score for heading: {heading} is {calculate_sentiment_score(heading)}")
    return jsonify(sentiment_score=calculate_sentiment_score(heading)), 200

@auth_blueprint.route('/static/<path:path>')
def send_static(path: str) -> Response:
    """
    Serve static files.

    Args:
        path (str): The path to the static file.

    Returns:
        Response: The static file.
    """
    return send_from_directory('static', path)
