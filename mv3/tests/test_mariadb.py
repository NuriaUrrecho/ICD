import os

import pytest
from sqlalchemy import create_engine, text


@pytest.mark.skipif(not os.getenv("MARIADB_TEST_URL"), reason="MARIADB_TEST_URL no configurada")
def test_mariadb_connection():
    engine = create_engine(os.environ["MARIADB_TEST_URL"])
    with engine.connect() as connection:
        assert connection.execute(text("SELECT 1")).scalar_one() == 1
        assert connection.execute(text("SELECT COUNT(*) FROM avisos")).scalar_one() >= 0
