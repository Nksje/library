# Quick Reference - Where OOP Concepts Are Shown

## Easy Navigation for Presentation

---

## ABSTRACTION

**File**: `models/book.py` - Lines 1-20

```python
from abc import ABC, abstractmethod

class Book(ABC):
    def __init__(self, title: str, author: str, year: int):
        ... subclass contract defined here ...

    @abstractmethod
    def get_info(self) -> str:
        pass  # ← Subclasses MUST implement

    @abstractmethod
    def to_dict(self) -> dict:
        pass  # ← Subclasses MUST implement
```

**Point to say**: "The abstract class defines what all books must do (get_info, to_dict) without specifying HOW. Subclasses fill in the details."

---

## INHERITANCE

**File**: `models/book.py` - Lines 45-75

```python
class PhysicalBook(Book):
    def __init__(self, title: str, author: str, year: int, pages: int):
        super().__init__(title, author, year)  # ← Call parent
        self._pages = pages  # ← Physical-specific

class EBook(Book):
    def __init__(self, title: str, author: str, year: int, size_mb: float):
        super().__init__(title, author, year)  # ← Call parent
        self._size_mb = size_mb  # ← EBook-specific
```

**Point to say**: "Both inherit `borrow()` and `return_book()` from Book. But each type has unique attributes. This avoids duplicating borrowing logic."

---

## POLYMORPHISM

**File**: `models/book.py` - Lines 50-75

```python
class PhysicalBook(Book):
    def get_info(self) -> str:
        return f"[Printed] {self._title} — {self._author} ({self._year}), {self._pages} pg."

class EBook(Book):
    def get_info(self) -> str:
        return f"[Electric] {self._title} — {self._author} ({self._year}), {self._size_mb} MB"
```

**Point to say**: "Same method `get_info()`, different outputs. No if statements needed —Python calls the right version automatically."

**Demo in main.py** - Line 22:

```python
lib.show_all()  # Internally: for book in books: print(book.get_info())
```

---

## ENCAPSULATION

**File**: `models/user.py` - Lines 1-30

```python
class User:
    def __init__(self, name: str, user_id: int):
        self._name = name  # ← PRIVATE (underscore)
        self._id = user_id  # ← PRIVATE
        self._borrowed_books: list = []  # ← Can't modify directly

    @property  # ← Read-only access
    def name(self):
        return self._name

    def get_borrowed(self) -> list:
        return list(self._borrowed_books)  # ← Returns COPY

    def borrow_book(self, book):  # ← Controlled modification
        book.borrow()  # Checks availability
        self._borrowed_books.append(book)
```

**Point to say**: "Users can't directly modify `_borrowed_books`. They must use `borrow_book()`, which validates the action first. This protects data integrity."

**Test validation** - `test_library.py` Line 44:

```python
def test_borrow_unavailable_book(self):
    """Can't borrow if already issues - encapsulation prevents this"""
```

---

## DESIGN PATTERN: Factory

**File**: `models/book.py` - Lines 25-42

```python
@staticmethod
def from_dict(data: dict) -> "Book":
    """Factory method: creates correct book type"""
    if data["type"] == "physical":
        book = PhysicalBook(...)
    elif data["type"] == "ebook":
        book = EBook(...)
    else:
        raise ValueError(f"Unknown book type: {data['type']}")
    book._is_available = data["is_available"]
    return book
```

**Point to say**: "When loading from JSON, we use the factory to create the correct type. Adding a new book type? Just update this method—everything else stays the same."

**Usage** - `models/library.py` Line 40:

```python
for book_data in data["books"]:
    library._books.append(Book.from_dict(book_data))  # ← Factory handles type
```

---

## UNIT TESTS

### Test Group 1: Borrowing (Encapsulation + Polymorphism)

**File**: `test_library.py` - Lines 12-48

```python
def test_borrow_book(self):
    """Encapsulation: book state changes correctly"""
    self.assertTrue(self.book.is_available)
    self.user.borrow_book(self.book)
    self.assertFalse(self.book.is_available)

def test_borrow_unavailable_book(self):
    """Encapsulation: can't violate business rules"""
    self.user.borrow_book(self.book)
    user2 = User("Bob", user_id=2)
    with self.assertRaises(ValueError):
        user2.borrow_book(self.book)  # Already taken!
```

### Test Group 2: Fine Calculation (Inheritance + Logic)

**File**: `test_library.py` - Lines 54-100

```python
def test_fine_calculation_overdue(self):
    """Loan tracking: days overdue calculated correctly"""
    due_date = date.today() - timedelta(days=5)
    loan = Loan(
        book_title="Test Book",
        user_name="Alice",
        borrow_date=date.today() - timedelta(days=10),
        due_date=due_date,
        return_date=date.today()
    )
    fine = calculate_fine(loan)
    self.assertGreater(fine, 0)  # Fine should apply
```

### Test Group 3: Integration (All OOP concepts)

**File**: `test_library.py` - Lines 104-125

```python
def test_librarian_lend_book(self):
    """Librarian (facade) + Library (data) + User (encapsulation)"""
    self.librarian.lend_book(self.user, self.book)
    self.assertIn(self.book, self.user.get_borrowed())
```

---

## DEMO SCRIPT (main.py)

**Run with**: `python main.py`

| Line  | What It Shows                                        |
| ----- | ---------------------------------------------------- |
| 1-9   | Library setup (abstraction: generic handling)        |
| 11-13 | Adding different book types (polymorphism)           |
| 15-16 | Librarian management (separation of concerns)        |
| 18-21 | Member registration (encapsulation)                  |
| 23-26 | Borrowing through librarian (factory + polymorphism) |
| 28    | Display using get_info() (polymorphism!)             |
| 31    | Return and fine calculation (business logic)         |
| 34-35 | Save/Load (serialization using factory)              |

---

## Summary Table

| Concept             | File              | Lines | Key Point                             |
| ------------------- | ----------------- | ----- | ------------------------------------- |
| **Abstraction**     | `models/book.py`  | 1-20  | Abstract base class defines contract  |
| **Inheritance**     | `models/book.py`  | 45-75 | PhysicalBook & EBook extend Book      |
| **Polymorphism**    | `models/book.py`  | 50-75 | Different get_info() per type         |
| **Encapsulation**   | `models/user.py`  | 1-30  | Private attributes, controlled access |
| **Factory Pattern** | `models/book.py`  | 25-42 | Type-agnostic object creation         |
| **Tests**           | `test_library.py` | All   | 14 meaningful unit tests              |
| **Demo**            | `main.py`         | All   | Full system workflow                  |

---

## Talking Points Quick Checklist

During presentation, reference these:

- [ ] "Abstraction hides complexity — Book class says WHAT to do, not HOW"
- [ ] "Inheritance avoids code duplication — borrow() logic in one place"
- [ ] "Polymorphism eliminates if-statements — right method called automatically"
- [ ] "Encapsulation protects data — can't corrupt borrowed_books without borrow_book()"
- [ ] "Factory pattern centralizes type creation — easy to add new book types"
- [ ] "14 unit tests validate all behaviors — catch regressions immediately"
- [ ] "Live demo shows everything working end-to-end"

---

## If Asked: "Prove Feature X Works"

**"Prove polymorphism"**: → Run `python main.py`, show different output for [Printed] vs [Electric]

**"Prove encapsulation"**: → Show `test_borrow_unavailable_book` test - demonstrates book availability is protected

**"Prove inheritance"**: → Show PhysicalBook and EBook both can borrow/return without duplicating code

**"Prove factory pattern"**: → Show how Book.from_dict() creates correct type without caller knowing

**"Prove tests work"**: → Run `python -m pytest test_library.py -v` → 14 passed
