import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import URL

db = SQLAlchemy()
csrf = CSRFProtect()


def _database_uri():
    if explicit := os.getenv("DATABASE_URL"):
        return explicit
    return URL.create(
        "mysql+pymysql",
        username=os.getenv("DB_USER", "avisos_app"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "cpd_avisos"),
        query={"charset": "utf8mb4"},
    )


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "solo-desarrollo-cambiar"),
        SQLALCHEMY_DATABASE_URI=_database_uri(),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        STUDENT_NAME=os.getenv("STUDENT_NAME", "Nombre configurable"),
        SERVER_IP=os.getenv("SERVER_IP", "IP configurable"),
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    csrf.init_app(app)

    from .api import api_bp
    from .web import web_bp

    csrf.exempt(api_bp)
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()
    return app
