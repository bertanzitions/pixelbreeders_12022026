from flask import Blueprint, request, jsonify
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Movie, Rating

reviews_bp = Blueprint('reviews', __name__)

# Return all movies rated by the user
@reviews_bp.route('/ratings', methods=['GET'])
@jwt_required()
def get_user_ratings():
    current_user_id = get_jwt_identity()

    # Query all ratings for this user and adds movie info
    user_ratings = Rating.query.filter_by(user_id=current_user_id).join(Movie).all()

    results = []
    for rating in user_ratings:
        results.append({
            "movie": {
                "tmdb_id": rating.movie.tmdb_id,
                "title": rating.movie.title,
                "poster_path": rating.movie.poster_path,
                "backdrop_path": rating.movie.backdrop_path,
                "release_date": rating.movie.release_date.strftime('%Y-%m-%d') if rating.movie.release_date else None,
                "rating": rating.score,
                "rating_id": rating.id
            }
        })

    return jsonify(results), 200


# Create a new rating (cascade to create Movie if not exists)
@reviews_bp.route('/ratings', methods=['POST'])
@jwt_required()
def create_rating():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    print(data)

    tmdb_id = data.get('tmdb_id')
    score = data.get('score')
    movie_data = data.get('movie_data') # dict

    if tmdb_id is None or score is None:
        return jsonify({'error': 'Missing tmdb_id or score'}), 400

    # Check if Movie exists; if not, create it
    movie = Movie.query.filter_by(tmdb_id=tmdb_id).first()

    if not movie:
        if not movie_data:
            return jsonify({'error': 'Movie not found locally and no data provided to create it'}), 400
        
        release_date = None
        if movie_data.get('release_date'):
            try:
                release_date = datetime.strptime(movie_data['release_date'], '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'Release date is not in the default pattern.'}), 400

        movie = Movie(
            tmdb_id=tmdb_id,
            title=movie_data.get('title', 'Unknown Title'),
            poster_path=movie_data.get('poster_path'),
            backdrop_path=movie_data.get('backdrop_path'),
            overview=movie_data.get('overview'),
            release_date=release_date
        )
        db.session.add(movie)
        db.session.commit()

    #  prevent duplicated rating
    existing_rating = Rating.query.filter_by(user_id=current_user_id, movie_id=movie.id).first()
    if existing_rating:
        return jsonify({'error': 'Rating already exists.'}), 409
    
    new_rating = Rating(
        user_id=current_user_id,
        movie_id=movie.id,
        score=score
    )
    db.session.add(new_rating)
    db.session.commit()

    return jsonify({
        'message': 'Rating created successfully',
        'tmdb_id': tmdb_id,
        'score': new_rating.score,
        'movie_data': movie_data
    }), 201


# Update the rating of a movie
@reviews_bp.route('/ratings/<int:tmdb_id>', methods=['PUT'])
@jwt_required()
def update_rating(tmdb_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    new_score = data.get('score')

    if new_score is None:
        return jsonify({'error': 'New score is required'}), 400

    # find movie by tmdb_id and get its rating
    movie = Movie.query.filter_by(tmdb_id=tmdb_id).first()
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404
    rating = Rating.query.filter_by(user_id=current_user_id, movie_id=movie.id).first()
    if not rating:
        return jsonify({'error': 'Rating not found'}), 404

    # update score
    rating.score = new_score
    
    db.session.commit()

    return jsonify({'message': 'Rating updated successfully', 'new_score': rating.score}), 200


# Delete a rating (movie is not deleted)
@reviews_bp.route('/ratings/<int:tmdb_id>', methods=['DELETE'])
@jwt_required()
def delete_rating(tmdb_id):
    current_user_id = get_jwt_identity()

    movie = Movie.query.filter_by(tmdb_id=tmdb_id).first()
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    rating = Rating.query.filter_by(user_id=current_user_id, movie_id=movie.id).first()
    if not rating:
        return jsonify({'error': 'Rating not found'}), 404

    db.session.delete(rating)
    db.session.commit()

    return jsonify({'message': 'Rating deleted successfully'}), 200