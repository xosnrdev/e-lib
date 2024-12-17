from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """
    Base model for User entity.

    Attributes:
        name (str): Name of the user.
        email (EmailStr): Email address of the user.
    """

    name: str = Field(..., json_schema_extra={"example": "John Doe"})
    email: EmailStr = Field(..., json_schema_extra={"example": "johndoe@example.com"})

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    """
    Model for creating a new User.
    """

    pass


class UserUpdate(BaseModel):
    """
    Model for updating an existing User.

    Attributes:
        name (str | None): New name for the user.
        email (EmailStr | None): New email address for the user.
    """

    name: str | None = Field(None, json_schema_extra={"example": "Jane Doe"})
    email: EmailStr | None = Field(
        None, json_schema_extra={"example": "janedoe@example.com"}
    )

    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    """
    Model representing a User in the system.

    Attributes:
        id (int): Unique identifier for the user.
        is_active (bool): Indicates if the user account is active.
    """

    id: int
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)
