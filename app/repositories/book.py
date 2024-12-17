from app.models.book import Book, BookCreate, BookUpdate


class BookRepository:
    """
    Repository for managing Book entities.
    """

    def __init__(self, data_store):
        """
        Initializes the BookRepository with a data store.

        Args:
            data_store (dict): In-memory data store for books.
        """
        self.data_store = data_store

    def create_book(self, book_create: BookCreate) -> Book:
        """
        Creates a new book.

        Args:
            book_create (BookCreate): Data for creating a new book.

        Returns:
            Book: The created book with a unique ID.
        """
        book = Book(id=self.data_store.book_id_seq, **book_create.model_dump())
        self.data_store.books[self.data_store.book_id_seq] = book
        self.data_store.book_id_seq += 1
        return book

    def get_book(self, book_id: int) -> Book | None:
        """
        Retrieves a book by ID.

        Args:
            book_id (int): The ID of the book to retrieve.

        Returns:
            Book | None: The book if found, else None.
        """
        return self.data_store.books.get(book_id)

    def update_book(self, book_id: int, book_update: BookUpdate) -> Book | None:
        """
        Updates an existing book's information.

        Args:
            book_id (int): The ID of the book to update.
            book_update (BookUpdate): The new data for the book.

        Returns:
            Book | None: The updated book if found, else None.
        """
        book = self.get_book(book_id)
        if book:
            updated_data = book.model_copy(update=book_update.model_dump(exclude_unset=True))
            self.data_store.books[book_id] = updated_data
            return updated_data
        return None

    def delete_book(self, book_id: int) -> bool:
        """
        Deletes a book from the data store.

        Args:
            book_id (int): The ID of the book to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        if book_id in self.data_store.books:
            del self.data_store.books[book_id]
            return True
        return False

    def mark_book_unavailable(self, book_id: int) -> Book | None:
        """
        Marks a book as unavailable.

        Args:
            book_id (int): The ID of the book to mark as unavailable.

        Returns:
            Book | None: The updated book if found and available, else None.
        """
        book = self.get_book(book_id)
        if book and book.is_available:
            book.is_available = False
            self.data_store.books[book_id] = book
            return book
        return None

    def mark_book_available(self, book_id: int) -> Book | None:
        """
        Marks a book as available.

        Args:
            book_id (int): The ID of the book to mark as available.

        Returns:
            Book | None: The updated book if found and unavailable, else None.
        """
        book = self.get_book(book_id)
        if book and not book.is_available:
            book.is_available = True
            self.data_store.books[book_id] = book
            return book
        return None
