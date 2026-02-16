from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    ratings = db.relationship('Rating', backref='user', lazy=True)

    def set_password(self, password):
        """Creates a hash for the password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)

    # these methods are for printing properly in terminal, not only a <models.User> for example
    def __repr__(self):
        return f'<User {self.email}>'


class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    poster_path = db.Column(db.String(255))
    backdrop_path = db.Column(db.String(255))
    release_date = db.Column(db.DateTime)
    overview = db.Column(db.Text)
    
    ratings = db.relationship('Rating', backref='movie', lazy=True)

    def __repr__(self):
        return f'<Movie {self.title}>'

class Rating(db.Model):
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # FK's
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    def __repr__(self):
        return f'<Rating {self.score}>'