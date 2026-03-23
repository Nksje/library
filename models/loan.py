from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Loan:
    book_title: str
    user_name: str
    borrow_date: date
    due_date: date
    return_date: Optional[date] = None

    @property
    def overdue_days(self) -> int:
        effective = self.return_date or date.today()
        return max(0, (effective - self.due_date).days)

    def to_dict(self) -> dict:
        return {
            "book_title": self.book_title,
            "user_name": self.user_name,
            "borrow_date": self.borrow_date.isoformat(),
            "due_date": self.due_date.isoformat(),
            "return_date": self.return_date.isoformat() if self.return_date else None,
        }

    @staticmethod
    def from_dict(data) -> "Loan":
        return Loan(
            book_title=data["book_title"],
            user_name=data["user_name"],
            borrow_date=date.fromisoformat(data["borrow_date"]),
            due_date=date.fromisoformat(data["due_date"]),
            return_date=date.fromisoformat(
                data["return_date"]) if data["return_date"] else None,
        )
