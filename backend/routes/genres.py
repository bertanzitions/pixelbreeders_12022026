import os
import requests
from flask import Blueprint, request, jsonify

genres_bp = Blueprint('genres', __name__)

TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
TMDB_BASE_URL = os.environ.get('TMDB_BASE_URL')

# Gets the list of genres, used list in front end selection inputs
@genres_bp.route('/', methods=['GET'])
def get_genres():
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}"
    }
    params = {
        "language": "en-US"
    }

    try:
        response = requests.get(f"{TMDB_BASE_URL}/genre/movie/list", headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        return jsonify(data.get('genres', [])), 200

    except requests.exceptions.RequestException as e:
        print(f"Error calling TMDB Genres API: {e}")
        if e.response is not None:
             return jsonify(e.response.json()), e.response.status_code
        return jsonify({'error': 'Failed to fetch genres from TMDB'}), 502