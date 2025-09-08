import os
import logging
from datetime import datetime
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import requests

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Enable CORS for all routes
CORS(app)

# External news API configuration
NEWS_API_URL = "https://newsapi.org/v2/everything"


def _get_news_api_key() -> str:
    """Retrieve the News API key from environment variables"""
    api_key = os.environ.get("NEWS_API_KEY")
    if not api_key:
        load_dotenv()
        api_key = os.environ.get("NEWS_API_KEY")
    if not api_key:
        raise RuntimeError("NEWS_API_KEY environment variable is not set")
    return api_key


def _fetch_gaming_news():
    """Fetch gaming news articles from the external API"""
    api_key = _get_news_api_key()

    params = {
        "q": "gaming",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": api_key,
    }

    response = requests.get(NEWS_API_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    def format_date(date_str: str) -> str:
        if not date_str:
            return ""
        try:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d %H:%M UTC")
        except ValueError:
            return date_str

    articles = [
        {
            "title": a.get("title"),
            "description": a.get("description"),
            "url": a.get("url"),
            "image": a.get("urlToImage"),
            "publishedAt": format_date(a.get("publishedAt")),
            "source": (a.get("source") or {}).get("name"),
        }
        for a in data.get("articles", [])
    ]
    return articles


# Error handler for 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "The requested resource was not found",
        "status_code": 404,
    }), 404


# Error handler for 400
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "error": "Bad Request",
        "message": "The request was invalid",
        "status_code": 400,
    }), 400


# Error handler for 500
@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal Server Error",
        "message": "An internal error occurred",
        "status_code": 500,
    }), 500


# Documentation page route
@app.route('/')
def documentation():
    return render_template('index.html')


# API Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "API is running successfully",
        "timestamp": "2025-09-01T00:00:00Z",
    })


@app.route('/api/gaming-news', methods=['GET'])
def gaming_news_api():
    """Fetch the latest gaming news articles as JSON"""
    try:
        articles = _fetch_gaming_news()
        return jsonify({"status": "success", "count": len(articles), "data": articles})
    except RuntimeError as e:
        return jsonify({"error": "Configuration Error", "message": str(e)}), 500
    except requests.RequestException as e:
        logging.error(f"Error fetching gaming news: {str(e)}")
        return jsonify({
            "error": "Bad Gateway",
            "message": "Failed to fetch gaming news",
        }), 502


@app.route('/gaming-news', methods=['GET'])
def gaming_news_page():
    """Render the latest gaming news articles"""
    try:
        articles = _fetch_gaming_news()
        return render_template('gaming_news.html', articles=articles)
    except RuntimeError as e:
        return render_template('error.html', message=str(e)), 500
    except requests.RequestException as e:
        logging.error(f"Error fetching gaming news: {str(e)}")
        return render_template('error.html', message="Failed to fetch gaming news"), 502


# Get API information
@app.route('/api/info', methods=['GET'])
def api_info():
    """Get API information"""
    return jsonify({
        "name": "Gaming News API",
        "version": "1.0.0",
        "description": "Fetch the latest gaming news from around the web",
        "endpoints": {
            "health": "/api/health",
            "gaming_news": "/api/gaming-news",
            "info": "/api/info",
        },
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

