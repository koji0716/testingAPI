# Gaming News API

A small Flask application that fetches the latest gaming news articles from [NewsAPI](https://newsapi.org/).

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the project root and add your API key and any debug variables:
   ```bash
   NEWS_API_KEY=your_api_key_here
   CODEZ=example_value  # optional
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
- **Debug environment:** `GET /api/debug-env` shows the value of the `CODEZ` environment variable.

## Environment

This application loads `NEWS_API_KEY` and other environment variables from the environment at runtime. For local development, values from a `.env` file are used if the variable is not already defined. On platforms like Vercel, simply define `NEWS_API_KEY` (and optionally `CODEZ`) in your project settings; no `.env` file is required.

## Deploy to Vercel

This repository is configured for deployment on [Vercel](https://vercel.com/):

1. Set `NEWS_API_KEY` in your Vercel project environment variables.
2. Install the Vercel CLI and log in:
   ```bash
   npm i -g vercel
   vercel login
   ```
3. Deploy the application:
   ```bash
   vercel --prod
   ```
