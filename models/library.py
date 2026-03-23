import json
import os
from models.book import Book


class Library:
    def __init__(self, name: str, filepath: str = "library_data.json"):
        self._name = name
        self._filepath = filepath
        self._books: list[Book] = []

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
        data = {
            "name": self._name,
            "books": [book.to_dict() for book in self._books],
        }
        with open(self._filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 Saved {len(self._books)} of books → {self._filepath}")

    @classmethod
    def load(cls, filepath: str = "library_data.json") -> "Library":
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        library = cls(data["name"], filepath)
        for book_data in data["books"]:
            library._books.append(Book.from_dict(book_data))

        print(f"📂 Loaded {len(library._books)} of books from {filepath}")
        return library
