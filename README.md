# NEWS Aggregator API

The News Aggregator API is a Flask-based service that allows users to register, log in, and access news articles from various categories. Users can also get sentiment scores for news headings. The API fetches news from Times of India RSS feeds, extracts details, and returns the articles along with their sentiment scores.


## Features

- **User Authentication**: Register and login functionality using JWT for secure access.
- **News Fetching**: Retrieve news articles from different categories.
- **Sentiment Analysis**: Calculate sentiment scores for news headings.

## Endpoints

1. **Register User**
    - **URL**: `/register`
    - **Method**: `POST`
    - **Request Headers**:
        - `Content-Type: application/json`
    - **Request Body**:
        ```json
        {
            "username": "user1",
            "password": "password"
        }
        ```
    - **Response**:
        ```json
        {
            "message": "User user1 created successfully."
        }
        ```

2. **Login User**
    - **URL**: `/login`
    - **Method**: `POST`
    - **Request Headers**:
        - `Content-Type: application/json`
    - **Request Body**:
        ```json
        {
            "username": "user1",
            "password": "password"
        }
        ```
    - **Response**:
        ```json
        {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIxIn0.eyJleHAiOjE2MjYwNjYwNzYsImlhdCI6MTYyNjA2NTQ3Nn0.7Z"
        }
        ```
3. **Get News**
    - **URL**: `/news/<category>`
    - **Method**: `GET`
    - **Request Headers**:
        - `Authorization: Bearer <access_token>`
    - **Response**:
        ```json
        {
            "news": [
                {
                    "title": "News Title",
                    "description": "News Description",
                    "image": "Image URL",
                    "sentiment": "Sentiment Score out of 5"  
                }
            ]
        }
        ```

4. **Get Sentiment**
    - **URL**: `/sentiment`
    - **Method**: `POST`
    - **Request Headers**:
        - `Content-Type: application/json`
        
    - **Request Body**:
        ```json
        {
            "heading": "News Heading"
        }
        ```

    - **Response**:
        ```json
        {
            "sentiment": "Sentiment Score out of 5"
        }
        ```
## News Categories
The available categories for news are as follows:

- india
- sports
- entertainment
- science
- world
- technology
- top-stories
- most-recent
- business
- us
- cricket
- life-style
- astrology
- nri
- environment
- education

## Setup

1. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the Flask app:
    ```bash
    python run.py
    ```

4. The app will be running at `http://127.0.0.1:5000/`.

## cURL Commands

1. Register User:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username":"test", "password":"test"}' http://127.0.0.1:5000/auth/register
    ```

2. Login User:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username":"test", "password":"test"}' http://127.0.0.1:5000/auth/login
    ```

3. Get News:
    ```bash
    curl -X GET -H "Authorization: Bearer <token>" http://127.0.0.1:5000/news/<category>
    ```

4. Get Sentiment:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"heading":"Example news heading"}' http://127.0.0.1:5000/auth/sentimentScore
    ```

## License

This project is licensed under the [DBaJ-NC-CFL](./LICENCE.md).