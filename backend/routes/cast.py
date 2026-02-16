# routes/cast.py
import os
import requests
from flask import Blueprint, request, jsonify

cast_bp = Blueprint('cast', __name__)

TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
TMDB_BASE_URL = os.environ.get('TMDB_BASE_URL')

@cast_bp.route('/<int:movie_id>', methods=['GET'])
def get_movie_cast(movie_id):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}"
    }
    
    params = {
        "language": "en-US"
    }

    try:
        response = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}/credits", headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        formatted_cast = []
        for member in data.get('cast', []):
            formatted_cast.append({
                "id": member.get('id'),
                "name": member.get('name'),
                "original_name": member.get('original_name'),
                "character": member.get('character'),
                "profile_path": f"https://image.tmdb.org/t/p/w200{member.get('profile_path')}" if member.get('profile_path') else None,
                "order": member.get('order'),
                "gender": member.get('gender'),
                "known_for_department": member.get('known_for_department'),
                "cast_id": member.get('cast_id'),
                "credit_id": member.get('credit_id')
            })
            
        return jsonify(formatted_cast), 200

    except requests.exceptions.RequestException as e:
        print(f"Error calling TMDB Credits API: {e}")
        if e.response is not None:
             return jsonify(e.response.json()), e.response.status_code
        return jsonify({'error': 'Failed to fetch cast from TMDB'}), 502