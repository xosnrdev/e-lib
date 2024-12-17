from .book import BookRepository
from .borrow import BorrowRepository
from .user import UserRepository


class DataStore:
    """
    In-memory data store for the application.

    Attributes:
        users (dict): Stores User entities.
        books (dict): Stores Book entities.
        borrow_records (dict): Stores BorrowRecord entities.
        user_id_seq (int): Sequence counter for user IDs.
        book_id_seq (int): Sequence counter for book IDs.
        borrow_id_seq (int): Sequence counter for borrow record IDs.
    """

    def __init__(self):
        self.users = {}
        self.books = {}
        self.borrow_records = {}
        self.user_id_seq = 1
        self.book_id_seq = 1
        self.borrow_id_seq = 1


# Initialize the in-memory data store
data_store = DataStore()

# Initialize repositories with shared data store
user_repository = UserRepository(data_store)
book_repository = BookRepository(data_store)
borrow_repository = BorrowRepository(data_store)
