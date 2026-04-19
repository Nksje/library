from abstractions.protocols import LibraryCatalog
from models.book import Book
from models.user import User


class Librarian:
    """Librarian manages the library and its operations"""

    def __init__(self, name: str, library: LibraryCatalog):
        self._name = name
        self._library = library
        self._members: list[User] = []

    @property
    def name(self):
        return self._name

    def register_member(self, user: User):
        """Register a new member to the library"""
        self._members.append(user)
        print(f"📋 Member registered: {user.name}")

    def lend_book(self, user: User, book: Book):
        """Lend a book to a member"""
        if user not in self._members:
            raise ValueError(f"User {user.name} is not registered")
        if not book.is_available:
            raise ValueError(f"Book '{book.title}' is not available")
        user.borrow_book(book)

    def receive_book(self, user: User, book: Book):
        """Receive a returned book from a member"""
        if user not in self._members:
            raise ValueError(f"User {user.name} is not registered")
        user.return_book(book)

    def get_available_books(self) -> list[Book]:
        """Get all available books in the library"""
        return self._library.available_books()

    def find_books_by_author(self, author: str) -> list[Book]:
        """Find books by author"""
        return self._library.find_by_author(author)

    def get_members(self) -> list[User]:
        """Get all registered members"""
        return list(self._members)

    def __repr__(self):
        return f"Librarian({self._name})"
