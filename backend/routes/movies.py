import os
import requests
from flask import Blueprint, request, jsonify
from extensions import cache

movies_bp = Blueprint('movies', __name__)

TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
TMDB_BASE_URL = os.environ.get('TMDB_BASE_URL')

# connects to the TMDB API and searches for movies
# a query string is mandatory (movie title), not year, page and genre have defaultss
@movies_bp.route('/search', methods=['GET'])
@cache.cached(timeout=86400, query_string=True) # 24h cache
def search_movies():
    query = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    year = request.args.get('year')
    genre_id = request.args.get('genre')

    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}"
    }

    params = {
        "query": query,
        "include_adult": "false",
        "language": "en-US",
        "page": page
    }

    if year:
        params["primary_release_year"] = year

    try:
        response = requests.get(f"{TMDB_BASE_URL}/search/movie", headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('results', []):
            if genre_id and int(genre_id) not in item.get('genre_ids', []):
                continue

            poster_url = f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}" if item.get('poster_path') else None
            
            results.append({
                "tmdb_id": item.get('id'),
                "title": item.get('title'),
                "poster_path": poster_url,
                "overview": item.get('overview'),
                "release_date": item.get('release_date'),
                "backdrop_path": item.get('backdrop_path')
            })
            
        return jsonify({
            'results': results,
            'page': data.get('page'),
            'total_pages': data.get('total_pages')
        }), 200

    except requests.exceptions.RequestException as e:
        if e.response is not None:
             return jsonify(e.response.json()), e.response.status_code
        return jsonify({'error': 'Failed to fetch data from TMDB'}), 502