from models import User, Movie, Rating

# test representation that looks ugly on terminal if it is not made
def test_models_repr():
    """Test the string representation of models for debugging."""
    
    user = User(email="test@repr.com")
    assert repr(user) == '<User test@repr.com>'

    movie = Movie(title="Inception")
    assert repr(movie) == '<Movie Inception>'

    rating = Rating(score=10)
    assert repr(rating) == '<Rating 10>'