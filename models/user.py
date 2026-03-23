from datetime import date, timedelta
from models.loan import Loan
from utils.fine_calculator import calculate_fine, fine_report

DEFAULT_LOAN_DAYS = 14


class User:
    def __init__(self, name: str, user_id: int):
        self._name = name
        self._id = user_id
        self._borrowed_books: list = []
        self._loans: list[Loan] = []

    @property
    def name(self):
        return self._name

    @property
    def user_id(self):
        return self._id

    def borrow_book(self, book, due_date: date = None):
        book.borrow()
        if due_date is None:
            due_date = date.today() + timedelta(days=DEFAULT_LOAN_DAYS)
        loan = Loan(
            book_title=book.title,
            user_name=self._name,
            borrow_date=date.today(),
            due_date=due_date,
        )
        self._borrowed_books.append(book)
        self._loans.append(loan)
        print(f"{self._name} took the book: {book.title} (срок сдачи: {due_date})")

    def return_book(self, book, return_date: date = None):
        if book not in self._borrowed_books:
            raise ValueError(
                "This book has not been checked out by this user.")
        if return_date is None:
            return_date = date.today()

        loan = next(
            (l for l in self._loans if l.book_title ==
             book.title and l.return_date is None),
            None
        )
        if loan:
            loan.return_date = return_date
            fine = calculate_fine(loan)
            print(fine_report(loan))
            if fine > 0:
                print(f"   ⚠️  Пожалуйста, оплатите пеню: {fine:.2f} €")

        book.return_book()
        self._borrowed_books.remove(book)
        print(f"{self._name} returned the book: {book.title}")

    def get_borrowed(self) -> list:
        return list(self._borrowed_books)

    def get_loans(self) -> list[Loan]:
        return list(self._loans)

    def __repr__(self):
        return f"User({self._id}, {self._name})"
