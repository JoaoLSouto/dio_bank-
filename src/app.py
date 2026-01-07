import os
from datetime import datetime

import click
import sqlalchemy as sa
from flask import Flask, current_app
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import db  # 👈 db vem de um lugar só


migrate = Migrate()
jwt = JWTManager()


# =========================
# MODELS
# =========================

class Role(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="role")


class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)

    role_id: Mapped[int] = mapped_column(sa.ForeignKey("role.id"))
    role: Mapped["Role"] = relationship(back_populates="users")

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username})"


class Post(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)
    created: Mapped[datetime] = mapped_column(
        sa.DateTime, server_default=sa.func.now()
    )

    author_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))


# =========================
# CLI COMMAND
# =========================

@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    with current_app.app_context():
        db.create_all()
    click.echo("Initialized the database.")


# =========================
# APP FACTORY
# =========================

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///blog.sqlite",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY="super-secret",
    )

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile("config.py", silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.cli.add_command(init_db_command)

    # blueprints
    from src.controllers import user, auth, role
    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)

    return app
