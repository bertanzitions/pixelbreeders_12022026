import pytest
from unittest.mock import patch, Mock
import requests

MOCK_SEARCH_RESULTS = {
    "page": 1,
    "total_pages": 5,
    "results": [
        {
            "id": 101,
            "title": "Batman Begins",
            "poster_path": "/batman.jpg",
            "overview": "Dark knight...",
            "release_date": "2005-06-15",
            "backdrop_path": "/bg.jpg",
            "genre_ids": [28, 80]  # 28=Action, 80=Crime
        },
        {
            "id": 102,
            "title": "Batman & Robin",
            "poster_path": None,  # Testing missing poster
            "overview": "Ice to meet you...",
            "release_date": "1997-06-20",
            "backdrop_path": "/bg2.jpg",
            "genre_ids": [878]    # 878=Sci-Fi (No Action)
        }
    ]
}

# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_search_movies_missing_query(client):
    """
    Test that the endpoint returns 400 if 'query' param is missing.
    """
    response = client.get('/movies/search')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Query parameter is required'


def test_search_movies_success(client):
    """
    Test a basic successful search. Verifies data formatting.
    """
    with patch('routes.movies.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_SEARCH_RESULTS
        mock_get.return_value = mock_response

        response = client.get('/movies/search?query=Batman')

        assert response.status_code == 200
        data = response.get_json()

        # Check structure
        assert data['page'] == 1
        assert len(data['results']) == 2
        
        # Check formatting of the first result
        movie1 = data['results'][0]
        assert movie1['title'] == "Batman Begins"
        assert movie1['poster_path'] == "https://image.tmdb.org/t/p/w500/batman.jpg"
        
        # Check formatting of the second result (None poster)
        movie2 = data['results'][1]
        assert movie2['poster_path'] is None


def test_search_movies_with_year_param(client):
    """
    Test that passing 'year' in the URL correctly adds 'primary_release_year'
    to the TMDB API parameters.
    """
    with patch('routes.movies.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": [], "page": 1, "total_pages": 1}
        mock_get.return_value = mock_response

        client.get('/movies/search?query=Batman&year=2005')

        # Verify the arguments passed to requests.get
        args, kwargs = mock_get.call_args
        params_sent = kwargs['params']
        
        assert params_sent['query'] == 'Batman'
        assert params_sent['primary_release_year'] == '2005'


def test_search_movies_filter_by_genre(client):
    """
    Test the INTERNAL Python logic that filters results by genre.
    We request Genre ID 28 (Action). 
    Movie 101 has it (Keep). Movie 102 does not (Discard).
    """
    with patch('routes.movies.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_SEARCH_RESULTS
        mock_get.return_value = mock_response

        # Search with genre=28
        response = client.get('/movies/search?query=Batman&genre=28')

        assert response.status_code == 200
        data = response.get_json()
        results = data['results']

        # Should only have 1 movie left (Batman Begins)
        assert len(results) == 1
        assert results[0]['tmdb_id'] == 101
        assert results[0]['title'] == "Batman Begins"


def test_search_movies_tmdb_error_response(client):
    """
    Test when TMDB returns a specific error (e.g., 422 Validation Failed).
    """
    with patch('routes.movies.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 422
        mock_response.json.return_value = {"errors": ["query must be provided"]}
        
        # Simulate raise_for_status raising an HTTPError
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        response = client.get('/movies/search?query=Empty')

        assert response.status_code == 422
        assert "errors" in response.get_json()


def test_search_movies_connection_failure(client):
    """
    Test a total network failure (ConnectionError).
    """
    with patch('routes.movies.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Offline")

        response = client.get('/movies/search?query=Fail')

        assert response.status_code == 502
        assert response.get_json()['error'] == 'Failed to fetch data from TMDB'

    
def test_search_movies_caching(client):
    """
    Test that repeated searches for the SAME query use the cache,
    but different queries trigger a new API call.
    """
    with patch('routes.movies.requests.get') as mock_get:
        # Setup the mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_SEARCH_RESULTS
        mock_get.return_value = mock_response

        # 1. First Search: "Batman" -> Cache Miss -> Hits API
        response1 = client.get('/movies/search?query=Batman')
        assert response1.status_code == 200
        assert mock_get.call_count == 1

        # 2. Second Search: "Batman" (Same Query) -> Cache Hit -> API NOT called
        response2 = client.get('/movies/search?query=Batman')
        assert response2.status_code == 200
        assert mock_get.call_count == 1  # Count stays at 1

        # 3. Third Search: "Superman" (Different Query) -> Cache Miss -> Hits API again
        # This confirms that 'query_string=True' is working correctly
        client.get('/movies/search?query=Superman')
        assert mock_get.call_count == 2  # Count goes up to 2