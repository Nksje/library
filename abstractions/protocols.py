from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from models.book import Book
    from models.loan import Loan


@runtime_checkable
class LibraryCatalog(Protocol):
    """Read-only catalog operations used by staff (ISP: narrow surface vs full Library)."""

    def find_by_author(self, author: str) -> list[Book]:
        ...

    def available_books(self) -> list[Book]:
        ...


class LibraryPersistence(Protocol):
    """Persistence boundary for library snapshots (DIP: Library depends on abstraction)."""

    def save(self, payload: dict) -> None:
        ...

    def load(self) -> dict:
        ...


class FinePolicy(Protocol):
    """Pluggable fine rules (OCP/DIP: User depends on policy, not concrete formula)."""

    def calculate(self, loan: Loan) -> float:
        ...
