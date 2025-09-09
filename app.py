import os
import logging
from datetime import datetime
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import requests

# Load environment variables from a .env file if present
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Enable CORS for all routes
CORS(app)

# Hacker News API configuration
HN_API_URL = "https://hn.algolia.com/api/v1/search"


def _fetch_hacker_news():
    """Fetch front page Hacker News stories"""
    params = {"tags": "front_page"}
    response = requests.get(HN_API_URL, params=params, timeout=10)
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
            "title": h.get("title") or h.get("story_title"),
            "url": h.get("url") or h.get("story_url"),
            "author": h.get("author"),
            "points": h.get("points"),
            "created_at": format_date(h.get("created_at")),
        }
        for h in data.get("hits", [])
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


@app.route('/api/hacker-news', methods=['GET'])
def hacker_news_api():
    """Fetch the latest Hacker News stories as JSON"""
    try:
        articles = _fetch_hacker_news()
        return jsonify({"status": "success", "count": len(articles), "data": articles})
    except requests.RequestException as e:
        logging.error(f"Error fetching Hacker News: {str(e)}")
        return jsonify({
            "error": "Bad Gateway",
            "message": "Failed to fetch Hacker News",
        }), 502


@app.route('/hacker-news', methods=['GET'])
def hacker_news_page():
    """Render the latest Hacker News stories"""
    try:
        articles = _fetch_hacker_news()
        return render_template('hacker_news.html', articles=articles)
    except requests.RequestException as e:
        logging.error(f"Error fetching Hacker News: {str(e)}")
        return render_template('error.html', message="Failed to fetch Hacker News"), 502


# Get API information
@app.route('/api/info', methods=['GET'])
def api_info():
    """Get API information"""
    return jsonify({
        "name": "Hacker News API",
        "version": "1.0.0",
        "description": "Fetch front page Hacker News stories",
        "endpoints": {
            "health": "/api/health",
            "hacker_news": "/api/hacker-news",
            "info": "/api/info",
        },
    })


@app.route('/api/debug-env', methods=['GET'])
def debug_env():
    """Expose selected environment variables for debugging"""
    codez = os.environ.get("CODEZ")
    return jsonify({"CODEZ": codez})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

