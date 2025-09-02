# Gaming News API

A small Flask application that fetches the latest gaming news articles from [NewsAPI](https://newsapi.org/).

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the project root and add your API key:
   ```bash
   NEWS_API_KEY=your_api_key_here
   ```
   You can obtain a free key by creating an account at [NewsAPI](https://newsapi.org/).

## Run

```bash
python main.py
```

The server will start on `http://localhost:5000`.

## Usage

- **JSON API:** `GET /api/gaming-news` returns the latest articles as JSON.
- **HTML page:** Visit `http://localhost:5000/gaming-news` to view articles formatted for the browser.
- **Health check:** `GET /api/health` confirms the API status.

## Environment

This application uses `python-dotenv` to load environment variables, making it easy to run in environments like Termux. Ensure the `.env` file or the `NEWS_API_KEY` environment variable is set before starting the server.
