from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class BorrowRecordBase(BaseModel):
    """
    Base model for BorrowRecord entity.

    Attributes:
        user_id (int): ID of the user who borrowed the book.
        book_id (int): ID of the borrowed book.
    """

    user_id: int = Field(..., json_schema_extra={"example": 1})
    book_id: int = Field(..., json_schema_extra={"example": 1})

    model_config = ConfigDict(from_attributes=True)


class BorrowRecordCreate(BorrowRecordBase):
    """
    Model for creating a new BorrowRecord.
    """

    pass


class BorrowRecord(BorrowRecordBase):
    """
    Model representing a BorrowRecord in the system.

    Attributes:
        id (int): Unique identifier for the borrow record.
        borrow_date (date): Date when the book was borrowed.
        return_date (date | None): Date when the book was returned.
    """

    id: int
    borrow_date: date
    return_date: date | None = None

    model_config = ConfigDict(from_attributes=True)
