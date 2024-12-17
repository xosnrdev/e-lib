from .book import BookRepository
from .borrow import BorrowRepository
from .user import UserRepository


# A single data store instance shared across repositories
class DataStore:
    def __init__(self):
        self.users = {}
        self.books = {}
        self.borrow_records = {}
        self.user_id_seq = 1
        self.book_id_seq = 1
        self.borrow_id_seq = 1


data_store = DataStore()

# Initialize repositories with shared data store
user_repository = UserRepository(data_store)
book_repository = BookRepository(data_store)
borrow_repository = BorrowRepository(data_store)
