from __future__ import annotations

from abstractions.protocols import LibraryPersistence
from models.book import Book
from services.json_library_persistence import JsonLibraryPersistence


class Library:
    def __init__(
        self,
        name: str,
        filepath: str = "library_data.json",
        persistence: LibraryPersistence | None = None,
    ):
        self._name = name
        self._filepath = filepath
        self._books: list[Book] = []
        self._persistence = persistence or JsonLibraryPersistence(filepath)

    def add_book(self, book: Book):
        self._books.append(book)
        print(f"The book is added: {book.title}")

    def find_by_author(self, author: str) -> list[Book]:
        return [b for b in self._books if author.lower() in b._author.lower()]

    def available_books(self) -> list[Book]:
        return [b for b in self._books if b.is_available]

    def show_all(self):
        print(f"Library: {self._name}")
        for book in self._books:
            print(" •", book.get_info())

    def save(self):
        payload = {
            "name": self._name,
            "books": [book.to_dict() for book in self._books],
        }
        self._persistence.save(payload)
        print(f"💾 Saved {len(self._books)} of books → {self._filepath}")

    @classmethod
    def load(
        cls,
        filepath: str = "library_data.json",
        persistence: LibraryPersistence | None = None,
    ) -> "Library":
        store = persistence or JsonLibraryPersistence(filepath)
        data = store.load()

        library = cls(data["name"], filepath, persistence=store)
        for book_data in data["books"]:
            library._books.append(Book.from_dict(book_data))

        print(f"📂 Loaded {len(library._books)} of books from {filepath}")
        return library
