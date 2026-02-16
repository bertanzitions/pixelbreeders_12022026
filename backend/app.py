import os
from flask import Flask, jsonify
from flask_cors import CORS
from extensions import db, cache, jwt, migrate
from routes.auth import auth_bp
from routes.review import reviews_bp
from routes.movies import movies_bp
from routes.genres import genres_bp
from routes.cast import cast_bp

def create_app(config_override=None):
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')

    redis_url = os.environ.get('CACHE_REDIS_URL')
    if redis_url:
        app.config['CACHE_TYPE'] = 'RedisCache'
        app.config['CACHE_REDIS_URL'] = redis_url
    else:
        app.config['CACHE_TYPE'] = 'SimpleCache'

    app.config['CACHE_DEFAULT_TIMEOUT'] = 300

    if config_override:
        app.config.update(config_override)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app) 

    app.register_blueprint(auth_bp, url_prefix='/auth') 
    app.register_blueprint(reviews_bp, url_prefix='/reviews') 
    app.register_blueprint(movies_bp, url_prefix='/movies') 
    app.register_blueprint(genres_bp, url_prefix='/genres') 
    app.register_blueprint(cast_bp, url_prefix='/cast') 

    @app.route('/', methods=['GET'])
    def hello():
        return jsonify({"msg": "Hello world!"}), 200
    
    return app

# Gunicorn for deploy needs it
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)