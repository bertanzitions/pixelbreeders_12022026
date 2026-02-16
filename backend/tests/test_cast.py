import pytest
from unittest.mock import patch, Mock
import requests

MOCK_TMDB_CAST_RESPONSE = {
    "id": 550,
    "cast": [
        {
            "adult": False,
            "gender": 2,
            "id": 819,
            "known_for_department": "Acting",
            "name": "Edward Norton",
            "original_name": "Edward Norton",
            "popularity": 26.99,
            "profile_path": "/5XBzD5wuTyVQZeS4VI25z2moMeY.jpg",
            "cast_id": 4,
            "character": "The Narrator",
            "credit_id": "52fe4250c3a36847f80149f3",
            "order": 0
        },
        {
            "adult": False,
            "gender": 2,
            "id": 287,
            "known_for_department": "Acting",
            "name": "Brad Pitt",
            "original_name": "Brad Pitt",
            "popularity": 45.66,
            "profile_path": None, # null image case
            "cast_id": 5,
            "character": "Tyler Durden",
            "credit_id": "52fe4250c3a36847f80149f7",
            "order": 1
        }
    ]
}
def test_get_movie_cast_success(client):
    """
    Test that the endpoint correctly fetches data from TMDB,
    formats the image URLs, and returns the simplified structure.
    """
    # We patch 'routes.cast.requests.get' because that is where requests is used
    with patch('routes.cast.requests.get') as mock_get:
        # Configure the mock to return a successful response (200 OK)
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_TMDB_CAST_RESPONSE
        mock_get.return_value = mock_response

        response = client.get('/cast/550')

        assert response.status_code == 200
        data = response.get_json()

        # Check that we got a list back
        assert isinstance(data, list)
        assert len(data) == 2

        # Check the first actor (Edward Norton) and formatted image
        actor1 = data[0]
        assert actor1['name'] == "Edward Norton"
        assert actor1['character'] == "The Narrator"
        # Validate logic: https://image.tmdb.org/t/p/w200 + profile_path
        assert actor1['profile_path'] == "https://image.tmdb.org/t/p/w200/5XBzD5wuTyVQZeS4VI25z2moMeY.jpg"

        # Check the second actor (Brad Pitt) and None image
        actor2 = data[1]
        assert actor2['name'] == "Brad Pitt"
        assert actor2['profile_path'] is None


def test_get_movie_cast_tmdb_404(client):
    """
    Test how the backend handles it when TMDB returns a 404 (Movie not found).
    """
    with patch('routes.cast.requests.get') as mock_get:
        # Configure the mock to simulate a 404 from TMDB
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"status_message": "The resource you requested could not be found."}
        
        # raise_for_status() must raise an HTTPError for the except block to catch it
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        
        mock_get.return_value = mock_response

        response = client.get('/cast/999999999')

        assert response.status_code == 404
        data = response.get_json()
        assert "status_message" in data


def test_get_movie_cast_tmdb_500(client):
    """
    Test how the backend handles an internal server error from TMDB.
    """
    with patch('routes.cast.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"status_message": "Internal Error"}
        
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        response = client.get('/cast/550')

        assert response.status_code == 500


def test_get_movie_cast_connection_error(client):
    """
    Test actual network failure (e.g., DNS failure, timeout) where
    requests.get raises an exception without a response object.
    """
    with patch('routes.cast.requests.get') as mock_get:
        # Simulate a total network failure
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")

        response = client.get('/cast/550')

        # The code explicitly returns 502 for generic RequestExceptions
        assert response.status_code == 502
        data = response.get_json()
        assert data['error'] == 'Failed to fetch cast from TMDB'


def test_get_movie_cast_empty_list(client):
    """
    Test a movie that exists but has no cast info.
    """
    with patch('routes.cast.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        # Return empty cast list
        mock_response.json.return_value = {"id": 1, "cast": []}
        mock_get.return_value = mock_response

        response = client.get('/cast/1')

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0