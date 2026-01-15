import os
from flask import Flask, json
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .config import DevelopmentConfig, ProductionConfig, TestingConfig
from .models import db
from .config import DevelopmentConfig, ProductionConfig
from flask_marshmallow import Marshmallow

migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
ma = Marshmallow()

def create_app(environment=None):
    if environment is None:
        environment = os.getenv("ENVIRONMENT", "development")

    app = Flask(__name__, instance_relative_config=True)

    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }

    app.config.from_object(config_map[environment])

    # instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    
    # blueprints
    from .controllers import user, auth, role

    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)

    from werkzeug.exceptions import HTTPException

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = e.get_response()
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        )
        response.content_type = "application/json"
        return response
    return app
