from fastapi import APIRouter, HTTPException, status

from app.models.borrow import BorrowRecord, BorrowRecordCreate
from app.repositories import book_repository, borrow_repository, user_repository

# Initialize repositories with data_store from app.main
router = APIRouter(prefix="/borrow", tags=["Borrow Operations"])


@router.post("/", response_model=BorrowRecord, status_code=status.HTTP_201_CREATED)
def borrow_book(borrow_data: BorrowRecordCreate):
    """
    Allows an active user to borrow an available book.

    **Endpoint:** POST /borrow/

    **Parameters:**
        - borrow_data (BorrowRecordCreate): The data containing `user_id` and `book_id`.

    **Responses:**
        - 201 Created: Book successfully borrowed.
        - 400 Bad Request: User is inactive or book is unavailable.
        - 404 Not Found: User or book does not exist.
        - 409 Conflict: Book already borrowed by the user.
    """
    # Validate user existence and status
    user = user_repository.get_user(borrow_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is inactive"
        )

    # Check if the user has already borrowed the book and hasn't returned it
    existing_borrow = borrow_repository.get_active_borrow_record(
        borrow_data.user_id, borrow_data.book_id
    )
    if existing_borrow:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Book already borrowed by the user",
        )

    # Validate book existence
    book = book_repository.get_book(borrow_data.book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    # Check if the book is available
    if not book.is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book is not available for borrowing",
        )

    # Proceed with borrowing the book
    borrow_record = borrow_repository.borrow_book(
        borrow_data.user_id, borrow_data.book_id
    )
    return borrow_record


@router.post("/return/{borrow_id}", response_model=BorrowRecord)
def return_book(borrow_id: int):
    """
    Marks a borrowed book as returned.

    **Endpoint:** POST /borrow/return/{borrow_id}

    **Parameters:**
        - borrow_id (int): The ID of the borrow record to update.

    **Responses:**
        - 200 OK: Book successfully returned.
        - 400 Bad Request: Cannot return book (e.g., already returned).
        - 404 Not Found: Borrow record does not exist.
    """
    borrow_record = borrow_repository.return_book(borrow_id)
    if not borrow_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot return book. Check if borrow record exists and book is not already returned.",
        )
    return borrow_record


@router.get("/records", response_model=list[BorrowRecord])
def get_all_borrow_records():
    """
    Retrieves all borrow records.

    **Endpoint:** GET /borrow/records

    **Responses:**
        - 200 OK: Returns a list of all borrow records.
    """
    return borrow_repository.get_all_borrow_records()


@router.get("/records/user/{user_id}", response_model=list[BorrowRecord])
def get_borrow_records_by_user(user_id: int):
    """
    Retrieves borrow records for a specific user.

    **Endpoint:** GET /borrow/records/user/{user_id}

    **Parameters:**
        - user_id (int): The ID of the user.

    **Responses:**
        - 200 OK: Returns a list of borrow records for the user.
        - 404 Not Found: User does not exist.
    """
    user = user_repository.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return borrow_repository.get_borrow_records_by_user(user_id)
