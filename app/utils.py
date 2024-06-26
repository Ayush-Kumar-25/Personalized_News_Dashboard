import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from typing import List, Dict, Any

# Download the VADER lexicon for sentiment analysis
nltk.download("vader_lexicon")

def extract_news_details(feed: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Extracts news details from the given feed.

    Args:
        feed (List[Dict[str, Any]]): The feed containing news items.

    Returns:
        List[Dict[str, str]]: A list of dictionaries with news details including heading, link, and image.
    """
    news_details: List[Dict[str, str]] = []
    seen_images: set[str] = set()

    for item in feed:
        if isinstance(item, dict):
            # Extract the heading, link, and summary from the item
            heading: str = item.get("title", "No title available")
            link: str = item.get("link", "#")
            summary: str = item.get("summary", "No summary available")
            image: str = ""

            # Extract image link if available
            links: List[Dict[str, str]] = item.get("links", [])
            if isinstance(links, list):
                for link_item in links:
                    if link_item.get("type", "").startswith("image"):
                        image_url = link_item.get("href", "")
                        if image_url not in seen_images:
                            seen_images.add(image_url)
                            break

            # Calculate the sentiment score
            sentiment_score: float = calculate_sentiment_score(heading)

            # Create a dictionary with the news details
            news: Dict[str, str] = {
                "heading": heading,
                "link": link,
                "summary": summary,
                "sentiment_score": sentiment_score,
                "image": image
            }
            news_details.append(news)
    return news_details

def calculate_sentiment_score(heading: str) -> float:
    """
    Calculates the sentiment score of a given heading.

    Args:
        heading (str): The heading for which to calculate the sentiment score.

    Returns:
        float: The calculated sentiment score, scaled and rounded to two decimal places.
    """
    # Initialize the SentimentIntensityAnalyzer
    sid: SentimentIntensityAnalyzer = SentimentIntensityAnalyzer()
    # Get the sentiment scores for the heading
    sentiment_score: float = sid.polarity_scores(heading)["compound"]
    # Scale and round the compound score to fit within the range 0 to 5
    return round((sentiment_score + 1) * 2.5, 2)
