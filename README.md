# Hacker News API

A small Flask application that fetches front page stories from [Hacker News](https://news.ycombinator.com/) using the public [Algolia API](https://hn.algolia.com/api).

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. (Optional) create a `.env` file to define debug variables such as `CODEZ`.

## Run

```bash
python main.py
```

The server will start on `http://localhost:5000`.

## Usage

- **JSON API:** `GET /api/hacker-news` returns the latest front page stories as JSON.
- **HTML page:** Visit `http://localhost:5000/hacker-news` to view stories formatted for the browser.
- **Health check:** `GET /api/health` confirms the API status.
- **Debug environment:** `GET /api/debug-env` shows the value of the `CODEZ` environment variable.

## Environment

This application requires no API keys. Environment variables are loaded from the environment at runtime. For local development, values from a `.env` file are used if the variable is not already defined.

## Deploy to Vercel

This repository is configured for deployment on [Vercel](https://vercel.com/):

1. Install the Vercel CLI and log in:
   ```bash
   npm i -g vercel
   vercel login
   ```
2. Deploy the application:
   ```bash
   vercel --prod
   ```
