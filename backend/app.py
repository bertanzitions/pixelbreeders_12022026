import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models import db
from routes.auth import auth_bp
from routes.review import reviews_bp
from routes.movies import movies_bp

def create_app(config_override=None):
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = "pixelbreeders"

    if config_override:
        app.config.update(config_override)

    jwt = JWTManager(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(auth_bp, url_prefix='/auth') 
    app.register_blueprint(reviews_bp, url_prefix='/reviews') 
    app.register_blueprint(movies_bp, url_prefix='/movies') 

    @app.route('/', methods=['GET'])
    def hello():
        return jsonify({"msg": "Hello world!"}), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)