import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def run_before_tests():
    """
    Fixture to run before each test.
    It resets the data_store to ensure test isolation.
    """
    from app.repositories import data_store

    data_store.users.clear()
    data_store.books.clear()
    data_store.borrow_records.clear()
    data_store.user_id_seq = 1
    data_store.book_id_seq = 1
    data_store.borrow_id_seq = 1
    yield


def test_health_check():
    # Arrange
    # No setup required as data_store is already reset

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "E-Library API System"
    assert data["version"] == "0.1.0"
    assert data["description"] == "API for managing an online library system"
    assert data["status"] == "operational"
    assert "system" in data
    assert "timestamp" in data
    assert isinstance(data["timestamp"], str)
    assert "os" in data["system"]
    assert "python_version" in data["system"]


def test_create_user():
    # Arrange
    user_data = {"name": "Alice", "email": "alice@example.com"}

    # Act
    response = client.post("/users/", json=user_data)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["is_active"] is True
    assert "id" in data
    assert data["id"] == 1


def test_get_user():
    # Arrange
    user_data = {"name": "Bob", "email": "bob@example.com"}
    client.post("/users/", json=user_data)

    # Act
    response = client.get("/users/1")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Bob"
    assert data["email"] == "bob@example.com"
    assert data["is_active"] is True
    assert data["id"] == 1


def test_update_user():
    # Arrange
    initial_user = {"name": "Charlie", "email": "charlie@example.com"}
    client.post("/users/", json=initial_user)
    updated_data = {"name": "Charles"}

    # Act
    response = client.put("/users/1", json=updated_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Charles"
    assert data["email"] == "charlie@example.com"


def test_deactivate_user():
    # Arrange
    user_data = {"name": "Diana", "email": "diana@example.com"}
    client.post("/users/", json=user_data)

    # Act
    response = client.patch("/users/1/deactivate")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] is False

    # Act (Attempt to deactivate again)
    response_duplicate = client.patch("/users/1/deactivate")

    # Assert
    assert response_duplicate.status_code == 400
    assert (
        response_duplicate.json()["detail"] == "User not found or already deactivated"
    )


def test_delete_user():
    # Arrange
    user_data = {"name": "Eve", "email": "eve@example.com"}
    client.post("/users/", json=user_data)

    # Act
    response = client.delete("/users/1")

    # Assert
    assert response.status_code == 204

    # Act (Attempt to get the deleted user)
    response_get = client.get("/users/1")

    # Assert
    assert response_get.status_code == 404


def test_create_book():
    # Arrange
    book_data = {"title": "1984", "author": "George Orwell"}

    # Act
    response = client.post("/books/", json=book_data)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "1984"
    assert data["author"] == "George Orwell"
    assert data["is_available"] is True
    assert "id" in data
    assert data["id"] == 1


def test_get_book():
    # Arrange
    book_data = {"title": "Brave New World", "author": "Aldous Huxley"}
    client.post("/books/", json=book_data)

    # Act
    response = client.get("/books/1")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Brave New World"
    assert data["author"] == "Aldous Huxley"
    assert data["is_available"] is True
    assert data["id"] == 1


def test_update_book():
    # Arrange
    initial_book = {"title": "Fahrenheit 451", "author": "Ray Bradbury"}
    client.post("/books/", json=initial_book)
    updated_data = {"title": "Fahrenheit Four Fifty-One"}

    # Act
    response = client.put("/books/1", json=updated_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Fahrenheit Four Fifty-One"
    assert data["author"] == "Ray Bradbury"


def test_mark_book_unavailable():
    # Arrange
    book_data = {"title": "The Catcher in the Rye", "author": "J.D. Salinger"}
    client.post("/books/", json=book_data)

    # Act
    response = client.patch("/books/1/mark_unavailable")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["is_available"] is False

    # Act (Attempt to mark again)
    response_duplicate = client.patch("/books/1/mark_unavailable")

    # Assert
    assert response_duplicate.status_code == 400
    assert (
        response_duplicate.json()["detail"]
        == "Book not found or already marked as unavailable"
    )


def test_mark_book_available():
    # Arrange
    book_data = {"title": "The Catcher in the Rye", "author": "J.D. Salinger"}
    client.post("/books/", json=book_data)
    client.patch("/books/1/mark_unavailable")

    # Act
    response = client.patch("/books/1/mark_available")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["is_available"] is True

    # Act (Attempt to mark again)
    response_duplicate = client.patch("/books/1/mark_available")

    # Assert
    assert response_duplicate.status_code == 400
    assert (
        response_duplicate.json()["detail"]
        == "Book not found or already marked as available"
    )


def test_delete_book():
    # Arrange
    book_data = {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}
    client.post("/books/", json=book_data)

    # Act
    response = client.delete("/books/1")

    # Assert
    assert response.status_code == 204

    # Act (Attempt to get the deleted book)
    response_get = client.get("/books/1")

    # Assert
    assert response_get.status_code == 404


def test_borrow_book():
    # Arrange
    user_data = {"name": "Frank", "email": "frank@example.com"}
    book_data = {"title": "To Kill a Mockingbird", "author": "Harper Lee"}
    client.post("/users/", json=user_data)
    client.post("/books/", json=book_data)

    # Act
    response = client.post("/borrow/", json={"user_id": 1, "book_id": 1})

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 1
    assert data["book_id"] == 1
    assert "id" in data
    assert data["id"] == 1
    assert "borrow_date" in data
    assert data["return_date"] is None

    # Act (Attempt to borrow the same book again)
    response_duplicate = client.post("/borrow/", json={"user_id": 1, "book_id": 1})

    # Assert
    assert response_duplicate.status_code == 409
    assert response_duplicate.json()["detail"] == "Book already borrowed by the user"


def test_borrow_book_inactive_user():
    # Arrange
    user_data = {"name": "Grace", "email": "grace@example.com"}
    book_data = {"title": "Moby Dick", "author": "Herman Melville"}
    client.post("/users/", json=user_data)
    client.patch("/users/1/deactivate")
    client.post("/books/", json=book_data)

    # Act
    response = client.post("/borrow/", json={"user_id": 1, "book_id": 1})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "User is inactive"


def test_borrow_unavailable_book():
    # Arrange
    user_data = {"name": "Hannah", "email": "hannah@example.com"}
    book_data = {"title": "War and Peace", "author": "Leo Tolstoy"}
    client.post("/users/", json=user_data)
    client.post("/books/", json=book_data)
    client.patch("/books/1/mark_unavailable")

    # Act
    response = client.post("/borrow/", json={"user_id": 1, "book_id": 1})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Book is not available for borrowing"


def test_return_book():
    # Arrange
    user_data = {"name": "Ian", "email": "ian@example.com"}
    book_data = {"title": "The Hobbit", "author": "J.R.R. Tolkien"}
    client.post("/users/", json=user_data)
    client.post("/books/", json=book_data)
    client.post("/borrow/", json={"user_id": 1, "book_id": 1})

    # Act
    response = client.post("/borrow/return/1")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["return_date"] is not None

    # Act (Attempt to return again)
    response_duplicate = client.post("/borrow/return/1")

    # Assert
    assert response_duplicate.status_code == 400
    assert (
        response_duplicate.json()["detail"]
        == "Cannot return book. Check if borrow record exists and book is not already returned."
    )


def test_get_all_borrow_records():
    # Arrange
    user1 = {"name": "Jack", "email": "jack@example.com"}
    user2 = {"name": "Karen", "email": "karen@example.com"}
    book1 = {"title": "Pride and Prejudice", "author": "Jane Austen"}
    book2 = {"title": "The Odyssey", "author": "Homer"}
    client.post("/users/", json=user1)
    client.post("/users/", json=user2)
    client.post("/books/", json=book1)
    client.post("/books/", json=book2)
    client.post("/borrow/", json={"user_id": 1, "book_id": 1})
    client.post("/borrow/", json={"user_id": 2, "book_id": 2})

    # Act
    response = client.get("/borrow/records")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["user_id"] == 1
    assert data[0]["book_id"] == 1
    assert data[1]["user_id"] == 2
    assert data[1]["book_id"] == 2


def test_get_borrow_records_by_user():
    # Arrange
    user1 = {"name": "Laura", "email": "laura@example.com"}
    user2 = {"name": "Mike", "email": "mike@example.com"}
    book1 = {"title": "The Alchemist", "author": "Paulo Coelho"}
    book2 = {"title": "The Little Prince", "author": "Antoine de Saint-Exupéry"}
    client.post("/users/", json=user1)
    client.post("/books/", json=book1)
    client.post("/books/", json=book2)
    client.post("/borrow/", json={"user_id": 1, "book_id": 1})
    client.post("/users/", json=user2)
    client.post("/borrow/", json={"user_id": 2, "book_id": 2})

    # Act
    response_user1 = client.get("/borrow/records/user/1")
    response_user2 = client.get("/borrow/records/user/2")

    # Assert for User 1
    assert response_user1.status_code == 200
    data_user1 = response_user1.json()
    assert len(data_user1) == 1
    assert data_user1[0]["user_id"] == 1
    assert data_user1[0]["book_id"] == 1

    # Assert for User 2
    assert response_user2.status_code == 200
    data_user2 = response_user2.json()
    assert len(data_user2) == 1
    assert data_user2[0]["user_id"] == 2
    assert data_user2[0]["book_id"] == 2


def test_borrow_nonexistent_user():
    # Arrange
    book_data = {"title": "The Catcher in the Rye", "author": "J.D. Salinger"}
    client.post("/books/", json=book_data)

    # Act
    response = client.post("/borrow/", json={"user_id": 999, "book_id": 1})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_borrow_nonexistent_book():
    # Arrange
    user_data = {"name": "Nina", "email": "nina@example.com"}
    client.post("/users/", json=user_data)

    # Act
    response = client.post("/borrow/", json={"user_id": 1, "book_id": 999})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_return_nonexistent_borrow_record():
    # Arrange
    # No setup required as the borrow record does not exist

    # Act
    response = client.post("/borrow/return/999")

    # Assert
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Cannot return book. Check if borrow record exists and book is not already returned."
    )
