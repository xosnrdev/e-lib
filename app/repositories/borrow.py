from datetime import date

from app.models.borrow import BorrowRecord


class BorrowRepository:
    """
    Repository for managing BorrowRecord entities.
    """

    def __init__(self, data_store):
        """
        Initializes the BorrowRepository with a data store.

        Args:
            data_store (dict): In-memory data store for borrow records.
        """
        self.data_store = data_store

    def borrow_book(self, user_id: int, book_id: int) -> BorrowRecord | None:
        """
        Allows a user to borrow a book.

        Args:
            user_id (int): ID of the user borrowing the book.
            book_id (int): ID of the book to be borrowed.

        Returns:
            BorrowRecord | None: The created borrow record if successful, else None.
        """
        user = self.data_store.users.get(user_id)
        book = self.data_store.books.get(book_id)
        if user and user.is_active and book and book.is_available:
            borrow_record = BorrowRecord(
                id=self.data_store.borrow_id_seq,
                user_id=user_id,
                book_id=book_id,
                borrow_date=date.today(),
            )
            self.data_store.borrow_records[self.data_store.borrow_id_seq] = borrow_record
            self.data_store.borrow_id_seq += 1

            # Update book availability
            book.is_available = False
            self.data_store.books[book_id] = book

            return borrow_record
        return None

    def return_book(self, borrow_id: int) -> BorrowRecord | None:
        """
        Marks a borrowed book as returned.

        Args:
            borrow_id (int): ID of the borrow record.

        Returns:
            BorrowRecord | None: The updated borrow record if successful, else None.
        """
        record = self.data_store.borrow_records.get(borrow_id)
        if record and record.return_date is None:
            record.return_date = date.today()
            self.data_store.borrow_records[borrow_id] = record

            # Update book availability
            book = self.data_store.books.get(record.book_id)
            if book:
                book.is_available = True
                self.data_store.books[book.id] = book

            return record
        return None

    def get_all_borrow_records(self) -> list[BorrowRecord]:
        """
        Retrieves all borrow records.

        Returns:
            List[BorrowRecord]: A list of all borrow records.
        """
        return list(self.data_store.borrow_records.values())

    def get_borrow_records_by_user(self, user_id: int) -> list[BorrowRecord]:
        """
        Retrieves borrow records for a specific user.

        Args:
            user_id (int): ID of the user.

        Returns:
            List[BorrowRecord]: A list of borrow records for the user.
        """
        return [
            record for record in self.data_store.borrow_records.values() if record.user_id == user_id
        ]

    def get_active_borrow_record(self, user_id: int, book_id: int) -> BorrowRecord | None:
        """
        Checks if a user has an active borrow record for a specific book.

        Args:
            user_id (int): ID of the user.
            book_id (int): ID of the book.

        Returns:
            BorrowRecord | None: The active borrow record if exists, else None.
        """
        for record in self.data_store.borrow_records.values():
            if (
                record.user_id == user_id
                and record.book_id == book_id
                and record.return_date is None
            ):
                return record
        return None
