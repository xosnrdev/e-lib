from fastapi import APIRouter, HTTPException, status

from app.models.user import User, UserCreate, UserUpdate
from app.repositories import user_repository

# Initialize repository with data_store from app.main
router = APIRouter(prefix="/users", tags=["User Endpoints"])


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_create: UserCreate):
    """
    Creates a new user.

    **Endpoint:** POST /users/

    **Parameters:**
        - user_create (UserCreate): The user data to create.

    **Responses:**
        - 201 Created: Returns the created user.
        - 400 Bad Request: Validation errors.
    """
    new_user = user_repository.create_user(user_create)
    return new_user


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    """
    Retrieves a user by ID.

    **Endpoint:** GET /users/{user_id}

    **Parameters:**
        - user_id (int): The ID of the user to retrieve.

    **Responses:**
        - 200 OK: Returns the user data.
        - 404 Not Found: User does not exist.
    """
    user = user_repository.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate):
    """
    Updates an existing user's information.

    **Endpoint:** PUT /users/{user_id}

    **Parameters:**
        - user_id (int): The ID of the user to update.
        - user_update (UserUpdate): The new data for the user.

    **Responses:**
        - 200 OK: Returns the updated user.
        - 404 Not Found: User does not exist.
    """
    updated_user = user_repository.update_user(user_id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """
    Deletes a user from the system.

    **Endpoint:** DELETE /users/{user_id}

    **Parameters:**
        - user_id (int): The ID of the user to delete.

    **Responses:**
        - 204 No Content: User successfully deleted.
        - 404 Not Found: User does not exist.
    """
    success = user_repository.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return


@router.patch("/{user_id}/deactivate", response_model=User)
def deactivate_user(user_id: int):
    """
    Deactivates a user by setting `is_active` to False.

    **Endpoint:** PATCH /users/{user_id}/deactivate

    **Parameters:**
        - user_id (int): The ID of the user to deactivate.

    **Responses:**
        - 200 OK: Returns the deactivated user.
        - 400 Bad Request: User already deactivated.
        - 404 Not Found: User does not exist.
    """
    user = user_repository.deactivate_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found or already deactivated",
        )
    return user
