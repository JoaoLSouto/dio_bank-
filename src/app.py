import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .config import DevelopmentConfig, ProductionConfig, TestingConfig
from .models import db
from .config import DevelopmentConfig, ProductionConfig

migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()


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

    # blueprints
    from .controllers import user, auth, role

    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)

    return app
