# tests/test_reviews.py
import pytest
from models import Movie, Rating, db

# ==============================================================================
# BASIC CRUD
# ==============================================================================

def test_create_rating_and_movie_cascade(client, user1_auth, app):
    """
    If a movie doesn't exist in the DB when rating,
    backend must create the Movie entry first, then the Rating.
    """
    payload = {
        "tmdb_id": 100,
        "score": 8,
        "movie_data": {
            "title": "New Movie",
            "poster_path": "/img.jpg",
            "release_date": "2023-01-01",
            "overview": "A test movie"
        }
    }

    response = client.post('/reviews/ratings', json=payload, headers=user1_auth)
    
    assert response.status_code == 201
    
    with app.app_context():
        # Verify Movie was created
        assert Movie.query.count() == 1
        movie = Movie.query.first()
        assert movie.title == "New Movie"
        
        # Verify Rating was created and linked
        assert Rating.query.count() == 1
        rating = Rating.query.first()
        assert rating.movie_id == movie.id
        assert rating.user_id == 1  # Matches user1_auth

def test_link_existing_movie(client, user1_auth, app):
    """
    If the movie ALREADY exists, the backend should NOT create a duplicate, but link it.
    """
    # manually create a movie in the DB
    with app.app_context():
        m = Movie(tmdb_id=200, title="Existing Movie")
        db.session.add(m)
        db.session.commit()

    # user rates this existing movie
    payload = {
        "tmdb_id": 200,  # the same as the created movie
        "score": 9,
        "movie_data": {"title": "Title", "release_date": "2020-01-01"} 
    }
    
    response = client.post('/reviews/ratings', json=payload, headers=user1_auth)
    assert response.status_code == 201

    with app.app_context():
        # Movie count should still be 1
        assert Movie.query.count() == 1 
        # The rating should be linked
        rating = Rating.query.first()
        assert rating.score == 9
        assert rating.movie.tmdb_id == 200

# ==============================================================================
# USER ISOLATION
# ==============================================================================

def test_users_data_is_independent(client, user1_auth, user2_auth, app):
    """
    User 1 and User 2 both rate the same movie.
    - User 1 should only see their own rating (GET).
    - User 2 should only see their own rating (GET).
    - Updating User 2's rating should not touch User 1's rating.
    """
    # Common movie data
    movie_payload = {
        "tmdb_id": 555,
        "movie_data": {"title": "Matrix", "release_date": "1999-03-31"}
    }

    # User 1 rates it 10/10
    client.post('/reviews/ratings', json={**movie_payload, "score": 10}, headers=user1_auth)
    
    # User 2 rates it 5/10
    client.post('/reviews/ratings', json={**movie_payload, "score": 5}, headers=user2_auth)

    # User 1 fetches ratings
    res1 = client.get('/reviews/ratings', headers=user1_auth)
    data1 = res1.get_json()
    assert len(data1) == 1
    assert data1[0]['movie']['rating'] == 10  # Should see 10, not 5

    # User 2 fetches ratings
    res2 = client.get('/reviews/ratings', headers=user2_auth)
    data2 = res2.get_json()
    assert len(data2) == 1
    assert data2[0]['movie']['rating'] == 5   # Should see 5, not 10

def test_user_cannot_delete_others_rating(client, user1_auth, user2_auth, app):
    """
    User 2 tries to delete a movie rating that belongs to User 1.
    Since User 2 hasn't rated this movie, the backend should return 404 (Not Found).
    It should NOT delete User 1's data.
    """
    # User 1 rates a movie
    client.post('/reviews/ratings', json={
        "tmdb_id": 666, 
        "score": 10, 
        "movie_data": {"title": "Devil Movie"}
    }, headers=user1_auth)

    # User 2 tries to DELETE the rating for tmdb_id=666
    response = client.delete('/reviews/ratings/666', headers=user2_auth)

    # Should fail because User 2 has no rating for this movie
    assert response.status_code == 404 
    assert "Rating not found" in response.get_json()['error']

    # Verify User 1's rating still exists
    with app.app_context():
        assert Rating.query.count() == 1

# ==============================================================================
# FRONTEND POSSIBLE FORMAT MISSING
# ==============================================================================

def test_missing_required_fields(client, user1_auth):
    """Frontend forgets to send 'score' or 'tmdb_id'"""
    res = client.post('/reviews/ratings', json={"score": 5}, headers=user1_auth)
    assert res.status_code == 400
    
    res = client.post('/reviews/ratings', json={"tmdb_id": 123}, headers=user1_auth)
    assert res.status_code == 400

def test_create_movie_without_metadata(client, user1_auth):
    """No title/poster data when rating a movie"""
    payload = {"tmdb_id": 999, "score": 5}
    res = client.post('/reviews/ratings', json=payload, headers=user1_auth)
    
    assert res.status_code == 400
    assert "no data provided" in res.get_json()['error']

def test_bad_date_format(client, user1_auth):
    """Date as '01-01-2022' (DD-MM-YYYY) instead of '2022-01-01'."""
    payload = {
        "tmdb_id": 777,
        "score": 5,
        "movie_data": {
            "title": "Bad Date Movie",
            "release_date": "01-01-2022" # Wrong format
        }
    }
    res = client.post('/reviews/ratings', json=payload, headers=user1_auth)
    
    assert res.status_code == 400
    assert "Release date is not in the default pattern" in res.get_json()['error']

def test_duplicate_rating_prevention(client, user1_auth):
    """Logic: User tries to POST a rating for a movie they already rated."""
    payload = {
        "tmdb_id": 888,
        "score": 5,
        "movie_data": {"title": "Repeat Movie"}
    }
    
    # 1st success
    client.post('/reviews/ratings', json=payload, headers=user1_auth)
    
    # 2nd conflict
    res = client.post('/reviews/ratings', json=payload, headers=user1_auth)
    
    assert res.status_code == 409  # Conflict
    assert "Rating already exists" in res.get_json()['error']

# ==============================================================================
# UPDATE / DELETE LOGIC
# ==============================================================================

def test_update_rating_score(client, user1_auth, app):
    """Logic: Happy path for PUT (Edit)."""
    # Setup
    client.post('/reviews/ratings', json={
        "tmdb_id": 101, 
        "score": 2, 
        "movie_data": {"title": "Bad Movie"}
    }, headers=user1_auth)

    # Update score from 2 to 5
    res = client.put('/reviews/ratings/101', json={"score": 5}, headers=user1_auth)
    
    assert res.status_code == 200
    assert res.get_json()['new_score'] == 5
    
    # Verify DB
    with app.app_context():
        rating = Rating.query.join(Movie).filter(Movie.tmdb_id == 101).first()
        assert rating.score == 5

def test_update_non_existent_movie(client, user1_auth):
    """Logic: Trying to update a movie that isn't in the database."""
    res = client.put('/reviews/ratings/999999', json={"score": 5}, headers=user1_auth)
    assert res.status_code == 404

def test_update_rating_missing_score_field(client, user1_auth):
    """
    Logic: PUT request must contain 'score'. 
    Covers line: if new_score is None: return ... 400
    """

    res = client.put('/reviews/ratings/123', json={"wrong_key": 10}, headers=user1_auth)
    
    assert res.status_code == 400
    assert "New score is required" in res.get_json()['error']

def test_update_rating_not_found_but_movie_exists(client, user1_auth, app):
    """
    Movie exists (e.g., added by someone else), but this user hasn't rated it yet.
    Covers line: if not rating: return ... 404 (inside update_rating)
    """
    # Manually create a movie
    with app.app_context():
        # Ensure we don't conflict with other tests using tmdb_id 300
        m = Movie(tmdb_id=300, title="Unrated Movie")
        db.session.add(m)
        db.session.commit()

    # User 1 tries to UPDATE a rating for this movie (but he never created one)
    res = client.put('/reviews/ratings/300', json={"score": 5}, headers=user1_auth)
    
    assert res.status_code == 404
    assert "Rating not found" in res.get_json()['error']

def test_delete_movie_not_found(client, user1_auth):
    """
    Try to delete a rating for a movie that doesn't exist in the DB at all.
    """
    res = client.delete('/reviews/ratings/999999', headers=user1_auth)
    
    assert res.status_code == 404
    assert "Movie not found" in res.get_json()['error']

def test_get_ratings_with_null_release_date(client, user1_auth):
    """
    Create a movie with NO release date to test the dictionary formatting.
    """
    # Create a rating for a movie with None as release_date
    payload = {
        "tmdb_id": 400,
        "score": 8,
        "movie_data": {
            "title": "Old Movie",
            "release_date": None, # Explicitly None
            "poster_path": "path.jpg"
        }
    }
    client.post('/reviews/ratings', json=payload, headers=user1_auth)

    # Get the ratings
    res = client.get('/reviews/ratings', headers=user1_auth)
    data = res.get_json()

    # Verify it didn't crash and returned None
    assert res.status_code == 200
    found_movie = next(item for item in data if item['movie']['tmdb_id'] == 400)
    assert found_movie['movie']['release_date'] is None

def test_delete_rating_success(client, user1_auth, app):
    """
    User successfully deletes a rating they created.
    """
    # User 1 rates a movie
    tmdb_id = 500
    client.post('/reviews/ratings', json={
        "tmdb_id": tmdb_id,
        "score": 8,
        "movie_data": {"title": "Delete Me"}
    }, headers=user1_auth)

    # User 1 deletes the rating
    res = client.delete(f'/reviews/ratings/{tmdb_id}', headers=user1_auth)

    assert res.status_code == 200
    assert res.get_json()['message'] == 'Rating deleted successfully'

    # Rating should be gone in DB
    with app.app_context():
        # The movie should still exist
        movie = Movie.query.filter_by(tmdb_id=tmdb_id).first()
        assert movie is not None
        
        # Rating for User 1 should be gone
        rating = Rating.query.filter_by(user_id=1, movie_id=movie.id).first()
        assert rating is None