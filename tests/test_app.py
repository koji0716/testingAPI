import os
import sys
import pytest
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app import app, _fetch_hacker_news


@pytest.fixture
def client():
    return app.test_client()


def test_health_endpoint(client):
    resp = client.get('/api/health')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['status'] == 'healthy'
    assert 'timestamp' in data


def test_hacker_news_api_endpoint(client):
    mock_articles = [
        {
            'title': 'Story',
            'url': 'https://example.com',
            'author': 'tester',
            'points': 123,
            'created_at': '2023-01-01 00:00 UTC',
        }
    ]
    with patch('app._fetch_hacker_news', return_value=mock_articles):
        resp = client.get('/api/hacker-news')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'success'
        assert data['count'] == 1
        assert data['data'] == mock_articles


def test_fetch_hacker_news_formats_data():
    sample_api_response = {
        'hits': [
            {
                'title': 'Hello',
                'url': 'https://example.com',
                'author': 'abc',
                'points': 1,
                'created_at': '2023-01-01T00:00:00.000Z',
            }
        ]
    }

    class MockResponse:
        def __init__(self, data):
            self._data = data

        def json(self):
            return self._data

        def raise_for_status(self):
            pass

    with patch('requests.get', return_value=MockResponse(sample_api_response)):
        articles = _fetch_hacker_news()
        assert articles == [
            {
                'title': 'Hello',
                'url': 'https://example.com',
                'author': 'abc',
                'points': 1,
                'created_at': '2023-01-01 00:00 UTC',
            }
        ]
