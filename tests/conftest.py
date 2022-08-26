import pytest
from app.server import create_app

@pytest.fixture
def client():
    app = create_app(config={"TESTING": True})
    with app.test_client() as client:
        yield client