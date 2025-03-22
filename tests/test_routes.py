import pytest

from app import create_app, db


@pytest.fixture
def client():
    app = create_app(testing=True)  # Ensure this configures an in-memory DB
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Reset database
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Clean up after test


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Welcome to the Flask API!"}


def test_register(client):
    response = client.post(
        "/register", json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 201
    assert response.get_json()["message"] == "User created successfully"


def test_login(client):
    client.post("/register",
                json={"username": "testuser", "password": "testpass"}
                )
    response = client.post(
        "/login", json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "token" in response.get_json()
