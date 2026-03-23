import unittest
from datetime import date, timedelta
from models.book import PhysicalBook, EBook
from models.user import User
from models.loan import Loan
from models.library import Library
from models.librarian import Librarian
from utils.fine_calculator import calculate_fine


class TestBorrowingLogic(unittest.TestCase):
    """Test borrowing and returning logic"""

    def setUp(self):
        """Set up test fixtures"""
        self.user = User("Alice", user_id=1)
        self.book = PhysicalBook("Clean Code", "Robert Martin", 2008, 464)

    def test_borrow_book(self):
        """Test that a user can borrow an available book"""
        self.assertTrue(self.book.is_available)
        self.user.borrow_book(self.book)
        self.assertFalse(self.book.is_available)
        self.assertIn(self.book, self.user.get_borrowed())

    def test_borrow_unavailable_book(self):
        """Test that borrowing an unavailable book raises error"""
        self.user.borrow_book(self.book)
        user2 = User("Bob", user_id=2)

        with self.assertRaises(ValueError):
            user2.borrow_book(self.book)

    def test_return_book(self):
        """Test that a user can return a borrowed book"""
        self.user.borrow_book(self.book)
        self.user.return_book(self.book)

        self.assertTrue(self.book.is_available)
        self.assertNotIn(self.book, self.user.get_borrowed())

    def test_return_unborowed_book(self):
        """Test that returning an unborrowed book raises error"""
        with self.assertRaises(ValueError):
            self.user.return_book(self.book)

    def test_loan_creation(self):
        """Test that a loan is created when borrowing"""
        self.user.borrow_book(self.book)
        loans = self.user.get_loans()

        self.assertEqual(len(loans), 1)
        self.assertEqual(loans[0].book_title, "Clean Code")
        self.assertEqual(loans[0].user_name, "Alice")


class TestOverdueLogic(unittest.TestCase):
    """Test overdue and fine calculation logic"""

    def setUp(self):
        """Set up test fixtures"""
        self.user = User("Alice", user_id=1)
        self.book = PhysicalBook("Clean Code", "Robert Martin", 2008, 464)

    def test_overdue_days_calculation(self):
        """Test that overdue days are calculated correctly"""
        due_date = date.today() - timedelta(days=5)
        loan = Loan(
            book_title="Test Book",
            user_name="Alice",
            borrow_date=date.today() - timedelta(days=10),
            due_date=due_date,
            return_date=date.today()
        )

        # overdue_days should be at least 5
        self.assertGreaterEqual(loan.overdue_days, 5)

    def test_no_overdue_before_due_date(self):
        """Test that no overdue days before due date"""
        due_date = date.today() + timedelta(days=5)
        loan = Loan(
            book_title="Test Book",
            user_name="Alice",
            borrow_date=date.today(),
            due_date=due_date,
        )

        self.assertEqual(loan.overdue_days, 0)

    def test_fine_calculation_zero_days(self):
        """Test that no fine is charged within grace period"""
        loan = Loan(
            book_title="Test Book",
            user_name="Alice",
            borrow_date=date.today(),
            due_date=date.today() + timedelta(days=1),
            return_date=date.today()
        )

        fine = calculate_fine(loan)
        self.assertEqual(fine, 0.0)

    def test_fine_calculation_overdue(self):
        """Test that fine is calculated for overdue books"""
        due_date = date.today() - timedelta(days=5)
        loan = Loan(
            book_title="Test Book",
            user_name="Alice",
            borrow_date=date.today() - timedelta(days=10),
            due_date=due_date,
            return_date=date.today()
        )

        fine = calculate_fine(loan)
        self.assertGreater(fine, 0)

    def test_fine_capped_at_maximum(self):
        """Test that fine is capped at the maximum"""
        due_date = date.today() - timedelta(days=100)
        loan = Loan(
            book_title="Test Book",
            user_name="Alice",
            borrow_date=date.today() - timedelta(days=120),
            due_date=due_date,
            return_date=date.today()
        )

        fine = calculate_fine(loan)
        self.assertLessEqual(fine, 20.0)  # MAX_FINE = 20.0


class TestLibraryIntegration(unittest.TestCase):
    """Test library and librarian integration"""

    def setUp(self):
        """Set up test fixtures"""
        self.library = Library("Test Library")
        self.librarian = Librarian("John", self.library)
        self.user = User("Alice", user_id=1)
        self.book = PhysicalBook("Clean Code", "Robert Martin", 2008, 464)

        self.library.add_book(self.book)
        self.librarian.register_member(self.user)

    def test_librarian_lend_book(self):
        """Test that librarian can lend a book"""
        self.librarian.lend_book(self.user, self.book)
        self.assertIn(self.book, self.user.get_borrowed())

    def test_librarian_get_available_books(self):
        """Test that librarian can view available books"""
        available = self.librarian.get_available_books()
        self.assertIn(self.book, available)

    def test_librarian_unregistered_user(self):
        """Test that lending to unregistered user fails"""
        unregistered_user = User("Bob", user_id=2)

        with self.assertRaises(ValueError):
            self.librarian.lend_book(unregistered_user, self.book)

    def test_librarian_find_books_by_author(self):
        """Test finding books by author"""
        books = self.librarian.find_books_by_author("Robert Martin")
        self.assertIn(self.book, books)


if __name__ == "__main__":
    unittest.main()
