import pytest

from inventario import create_app, db


@pytest.fixture()
def app(tmp_path):
    database = tmp_path / "test.sqlite"
    app = create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database}",
        "SECRET_KEY": "test-only",
    })
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()

