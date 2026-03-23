from abc import ABC, abstractmethod


class Book(ABC):
    def __init__(self, title: str, author: str, year: int):
        self._title = title
        self._author = author
        self._year = year
        self._is_available = True

    @property
    def title(self):
        return self._title

    @property
    def is_available(self):
        return self._is_available

    def borrow(self):
        if not self._is_available:
            raise ValueError(f"The book '{self._title}' is already issued.")
        self._is_available = False

    def return_book(self):
        self._is_available = True

    @abstractmethod
    def get_info(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @staticmethod
    def from_dict(data: dict) -> "Book":
        if data["type"] == "physical":
            book = PhysicalBook(
                data["title"], data["author"], data["year"], data["pages"])
        elif data["type"] == "ebook":
            book = EBook(data["title"], data["author"],
                         data["year"], data["size_mb"])
        else:
            raise ValueError(f"Unknown book type: {data['type']}")
        book._is_available = data["is_available"]
        return book


class PhysicalBook(Book):
    def __init__(self, title: str, author: str, year: int, pages: int):
        super().__init__(title, author, year)
        self._pages = pages

    def get_info(self) -> str:
        status = "available" if self._is_available else "issued"
        return (f"[Printed] {self._title} — {self._author} "
                f"({self._year}), {self._pages} pg. [{status}]")

    def to_dict(self) -> dict:
        return {
            "type": "physical",
            "title": self._title,
            "author": self._author,
            "year": self._year,
            "pages": self._pages,
            "is_available": self._is_available,
        }


class EBook(Book):
    def __init__(self, title: str, author: str, year: int, size_mb: float):
        super().__init__(title, author, year)
        self._size_mb = size_mb

    def get_info(self) -> str:
        status = "available" if self._is_available else "issued"
        return (f"[Electric] {self._title} — {self._author} "
                f"({self._year}), {self._size_mb} MB [{status}]")

    def to_dict(self) -> dict:
        return {
            "type": "ebook",
            "title": self._title,
            "author": self._author,
            "year": self._year,
            "size_mb": self._size_mb,
            "is_available": self._is_available,
        }
