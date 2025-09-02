import os
import logging
from flask import Flask, jsonify, render_template
from flask_cors import CORS
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


# Gaming news endpoint
@app.route('/api/gaming-news', methods=['GET'])
def gaming_news():
    """Fetch the latest gaming news articles"""
    api_key = os.environ.get("NEWS_API_KEY")
    if not api_key:
        return jsonify({
            "error": "Configuration Error",
            "message": "NEWS_API_KEY environment variable is not set",
        }), 500

    params = {
        "q": "gaming",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": api_key,
    }

    try:
        response = requests.get(NEWS_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        simplified = [
            {
                "title": a.get("title"),
                "description": a.get("description"),
                "url": a.get("url"),
                "publishedAt": a.get("publishedAt"),
                "source": (a.get("source") or {}).get("name"),
            }
            for a in articles
        ]
        return jsonify({"status": "success", "count": len(simplified), "data": simplified})
    except requests.RequestException as e:
        logging.error(f"Error fetching gaming news: {str(e)}")
        return jsonify({
            "error": "Bad Gateway",
            "message": "Failed to fetch gaming news",
        }), 502


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

