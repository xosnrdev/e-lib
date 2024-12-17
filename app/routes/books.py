from fastapi import APIRouter, HTTPException, status

from app.models.book import Book, BookCreate, BookUpdate
from app.repositories import book_repository

# Initialize repository with data_store from app.main
router = APIRouter(prefix="/books", tags=["Book Endpoints"])


@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book_create: BookCreate):
    """
    Creates a new book.

    **Endpoint:** POST /books/

    **Parameters:**
        - book_create (BookCreate): The book data to create.

    **Responses:**
        - 201 Created: Returns the created book.
        - 400 Bad Request: Validation errors.
    """
    new_book = book_repository.create_book(book_create)
    return new_book


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int):
    """
    Retrieves a book by ID.

    **Endpoint:** GET /books/{book_id}

    **Parameters:**
        - book_id (int): The ID of the book to retrieve.

    **Responses:**
        - 200 OK: Returns the book data.
        - 404 Not Found: Book does not exist.
    """
    book = book_repository.get_book(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return book


@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book_update: BookUpdate):
    """
    Updates an existing book's information.

    **Endpoint:** PUT /books/{book_id}

    **Parameters:**
        - book_id (int): The ID of the book to update.
        - book_update (BookUpdate): The new data for the book.

    **Responses:**
        - 200 OK: Returns the updated book.
        - 404 Not Found: Book does not exist.
    """
    updated_book = book_repository.update_book(book_id, book_update)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return updated_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    """
    Deletes a book from the system.

    **Endpoint:** DELETE /books/{book_id}

    **Parameters:**
        - book_id (int): The ID of the book to delete.

    **Responses:**
        - 204 No Content: Book successfully deleted.
        - 404 Not Found: Book does not exist.
    """
    success = book_repository.delete_book(book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return


@router.patch("/{book_id}/mark_unavailable", response_model=Book)
def mark_book_unavailable(book_id: int):
    """
    Marks a book as unavailable.

    **Endpoint:** PATCH /books/{book_id}/mark_unavailable

    **Parameters:**
        - book_id (int): The ID of the book to mark as unavailable.

    **Responses:**
        - 200 OK: Returns the updated book.
        - 400 Bad Request: Book already unavailable.
        - 404 Not Found: Book does not exist.
    """
    book = book_repository.mark_book_unavailable(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book not found or already marked as unavailable",
        )
    return book


@router.patch("/{book_id}/mark_available", response_model=Book)
def mark_book_available(book_id: int):
    """
    Marks a book as available.

    **Endpoint:** PATCH /books/{book_id}/mark_available

    **Parameters:**
        - book_id (int): The ID of the book to mark as available.

    **Responses:**
        - 200 OK: Returns the updated book.
        - 400 Bad Request: Book already available.
        - 404 Not Found: Book does not exist.
    """
    book = book_repository.mark_book_available(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book not found or already marked as available",
        )
    return book
