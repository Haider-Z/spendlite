import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


def test_create_expense():
    response = client.post(
        "/api/expenses/",
        json={
            "title": "Lunch",
            "amount": 500,
            "category": "Food",
            "date": "2026-10-30"
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Lunch"


def test_get_expenses():
    client.post(
        "/api/expenses/",
        json={
            "title": "Transport",
            "amount": 200,
            "category": "Transport",
            "date": "2026-10-30"
        }
    )

    response = client.get("/api/expenses/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_delete_expense():
    create_response = client.post(
        "/api/expenses/",
        json={
            "title": "Shopping",
            "amount": 1000,
            "category": "Shopping",
            "date": "2026-10-30"
        }
    )

    expense_id = create_response.json()["id"]

    response = client.delete(f"/api/expenses/{expense_id}")

    assert response.status_code == 200


def test_invalid_expense():
    response = client.post(
        "/api/expenses/",
        json={
            "title": "Invalid",
            "amount": -100,
            "category": "Food",
            "date": "2026-10-30"
        }
    )

    assert response.status_code == 422
