import pytest
from unittest.mock import patch, Mock
import requests

# ----------------------------------------------------------------------
# Helper: Sample Data
# ----------------------------------------------------------------------

MOCK_GENRES_RESPONSE = {
    "genres": [
        {"id": 28, "name": "Action"},
        {"id": 12, "name": "Adventure"},
        {"id": 16, "name": "Animation"}
    ]
}

# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_get_genres_success(client):
    """
    Test that the endpoint correctly fetches genres from TMDB
    and returns the list.
    """
    # Patch requests.get inside the routes.genres module
    with patch('routes.genres.requests.get') as mock_get:
        # Configure the mock to return success
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_GENRES_RESPONSE
        mock_get.return_value = mock_response

        # Request to our API
        response = client.get('/genres/')

        # Assertions
        assert response.status_code == 200
        data = response.get_json()

        # Verify data structure
        assert isinstance(data, list)
        assert len(data) == 3
        assert data[0]['name'] == 'Action'
        assert data[0]['id'] == 28

        # Ensure the API was actually called (not cached from a previous run)
        mock_get.assert_called_once()


def test_get_genres_caching(client):
    """
    Test that the second call to the endpoint does NOT hit the API
    (verifies that @cache.cached is working).
    """
    with patch('routes.genres.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_GENRES_RESPONSE
        mock_get.return_value = mock_response

        # First Call: Should hit the API
        response1 = client.get('/genres/')
        assert response1.status_code == 200
        assert mock_get.call_count == 1

        # Second Call: Should hit the Cache (API NOT called again)
        response2 = client.get('/genres/')
        assert response2.status_code == 200
        assert mock_get.call_count == 1  # Count should remain 1


def test_get_genres_tmdb_error(client):
    """
    Test handling of TMDB API errors (e.g., 401 Unauthorized, 500 Server Error).
    """
    with patch('routes.genres.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"status_message": "Invalid API key"}
        
        # We must manually simulate raise_for_status behavior
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        
        mock_get.return_value = mock_response

        response = client.get('/genres/')

        assert response.status_code == 401
        data = response.get_json()
        assert "Invalid API key" in data.get('status_message', '')


def test_get_genres_connection_error(client):
    """
    Test handling of network failures (e.g., DNS issues).
    """
    with patch('routes.genres.requests.get') as mock_get:
        # Simulate a crash in the requests library
        mock_get.side_effect = requests.exceptions.ConnectionError("TMDB Unreachable")

        response = client.get('/genres/')

        assert response.status_code == 502
        data = response.get_json()
        assert data['error'] == 'Failed to fetch genres from TMDB'