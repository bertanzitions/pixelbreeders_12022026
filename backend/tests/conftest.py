import sys
import os
import pytest
from flask import Response
from extensions import cache

# Add the project root to Python's path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from models import User
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    """Configures a new app mockup for each test"""
    
    # Hide Redis from the app logic
    old_redis_url = os.environ.get('CACHE_REDIS_URL')
    if 'CACHE_REDIS_URL' in os.environ:
        del os.environ['CACHE_REDIS_URL']

    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret-key",
        "CACHE_TYPE": "SimpleCache", 
        "CACHE_DEFAULT_TIMEOUT": 300
    }

    app = create_app(config_override=test_config)

    with app.app_context():
        cache.clear()
        db.drop_all()   
        db.create_all()
        
        yield app
        
        db.session.remove()
        db.drop_all()

    # Restore Redis URL
    if old_redis_url:
        os.environ['CACHE_REDIS_URL'] = old_redis_url

@pytest.fixture
def client(app):
    app.response_class = Response
    return app.test_client()

@pytest.fixture
def user1_auth(app):
    with app.app_context():
        user = User(email="user1@test.com", id=1)
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=str(user.id))
        return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def user2_auth(app):
    with app.app_context():
        user = User(email="user2@test.com", id=2)
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=str(user.id))
        return {'Authorization': f'Bearer {token}'}