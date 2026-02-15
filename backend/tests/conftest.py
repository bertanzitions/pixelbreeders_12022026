import sys
import os
import pytest

# Add the project root to Python's path
# This allows 'from app import...' to work from inside the tests/ folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from models import User
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    """Configures a new app mockup for each test"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret-key"
    })

    with app.app_context():
        db.drop_all()   # delete everything from the previous run
        db.create_all()
        
        yield app
        
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

# create two users, essential for test_review
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