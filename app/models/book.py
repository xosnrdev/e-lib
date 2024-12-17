from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    """
    Base model for Book entity.

    Attributes:
        title (str): Title of the book.
        author (str): Author of the book.
    """

    title: str = Field(..., json_schema_extra={"example": "The Great Gatsby"})
    author: str = Field(..., json_schema_extra={"example": "F. Scott Fitzgerald"})

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BookBase):
    """
    Model for creating a new Book.
    """

    pass


class BookUpdate(BaseModel):
    """
    Model for updating an existing Book.

    Attributes:
        title (str | None): New title for the book.
        author (str | None): New author for the book.
    """

    title: str | None = Field(None, json_schema_extra={"example": "The Great Gatsby"})
    author: str | None = Field(
        None, json_schema_extra={"example": "F. Scott Fitzgerald"}
    )

    model_config = ConfigDict(from_attributes=True)


class Book(BookBase):
    """
    Model representing a Book in the system.

    Attributes:
        id (int): Unique identifier for the book.
        is_available (bool): Indicates if the book is available for borrowing.
    """

    id: int
    is_available: bool = True

    model_config = ConfigDict(from_attributes=True)
