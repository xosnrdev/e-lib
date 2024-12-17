from app.models.user import User, UserCreate, UserUpdate


class UserRepository:
    """
    Repository for managing User entities.
    """

    def __init__(self, data_store):
        """
        Initializes the UserRepository with a data store.

        Args:
            data_store (dict): In-memory data store for users.
        """
        self.data_store = data_store

    def create_user(self, user_create: UserCreate) -> User:
        """
        Creates a new user.

        Args:
            user_create (UserCreate): Data for creating a new user.

        Returns:
            User: The created user with a unique ID.
        """
        user = User(id=self.data_store.user_id_seq, **user_create.model_dump())
        self.data_store.users[self.data_store.user_id_seq] = user
        self.data_store.user_id_seq += 1
        return user

    def get_user(self, user_id: int) -> User | None:
        """
        Retrieves a user by ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User | None: The user if found, else None.
        """
        return self.data_store.users.get(user_id)

    def update_user(self, user_id: int, user_update: UserUpdate) -> User | None:
        """
        Updates an existing user's information.

        Args:
            user_id (int): The ID of the user to update.
            user_update (UserUpdate): The new data for the user.

        Returns:
            User | None: The updated user if found, else None.
        """
        user = self.get_user(user_id)
        if user:
            updated_data = user.model_copy(update=user_update.model_dump(exclude_unset=True))
            self.data_store.users[user_id] = updated_data
            return updated_data
        return None

    def delete_user(self, user_id: int) -> bool:
        """
        Deletes a user from the data store.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        if user_id in self.data_store.users:
            del self.data_store.users[user_id]
            return True
        return False

    def deactivate_user(self, user_id: int) -> User | None:
        """
        Deactivates a user by setting `is_active` to False.

        Args:
            user_id (int): The ID of the user to deactivate.

        Returns:
            User | None: The deactivated user if found and active, else None.
        """
        user = self.get_user(user_id)
        if user and user.is_active:
            user.is_active = False
            self.data_store.users[user_id] = user
            return user
        return None
