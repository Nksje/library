# Library Management System - Presentation & Defence Script

## Part 1: Project Overview (2-3 minutes)

### Opening

"This is a **Library Management System** - a small but complete OOP project. Users can borrow books, return them, and the system automatically calculates late fees. Librarians manage members and book availability."

### Core Features

1. **Book Management**: Physical books and eBooks with different properties
2. **User Management**: Members can borrow up to multiple books
3. **Loan Tracking**: Automatic fine calculation for overdue returns
4. **Persistence**: Data saved to JSON and loaded on restart

---

## Part 2: OOP Pillars Demonstration (4-5 minutes)

### Pillar 1: Abstraction

**Explain**: "Abstraction hides complexity. We created an abstract `Book` class that doesn't specify whether a book is physical or digital."

```python
# Show this code:
from abc import ABC, abstractmethod

class Book(ABC):
    @abstractmethod
    def get_info(self) -> str:
        pass  # Subclasses MUST implement
```

**Say**: "The abstract class says: 'All books must have a `get_info()` method, but HOW they display info is up to subclasses.' This lets us add new book types without modifying existing code."

---

### Pillar 2: Inheritance

**Explain**: "Inheritance lets us reuse code. Both PhysicalBook and EBook inherit borrowing/returning logic from Book."

```python
# Show this code:
class PhysicalBook(Book):
    def __init__(self, title: str, author: str, year: int, pages: int):
        super().__init__(title, author, year)  # Call parent
        self._pages = pages

class EBook(Book):
    def __init__(self, title: str, author: str, year: int, size_mb: float):
        super().__init__(title, author, year)  # Call parent
        self._size_mb = size_mb
```

**Say**: "Both inherit `borrow()` and `return_book()` from the parent. But each type stores different data (pages vs file size). This avoids duplicating borrowing logic."

---

### Pillar 3: Polymorphism

**Explain**: "Polymorphism means 'many forms'. The same method call produces different results."

```python
# Show this code:
class PhysicalBook(Book):
    def get_info(self) -> str:
        return f"[Printed] {self._title} — {self._author}, {self._pages} pg."

class EBook(Book):
    def get_info(self) -> str:
        return f"[Electric] {self._title} — {self._author}, {self._size_mb} MB"

# Usage (no if statements!):
books = [physical_book, ebook]
for book in books:
    print(book.get_info())  # Correct version called automatically
```

**Say**: "Notice we don't need `if isinstance(book, PhysicalBook)`. Python calls the right `get_info()` automatically. If we add AudioBook later, we just implement its `get_info()` - no changes to existing code!"

---

### Pillar 4: Encapsulation

**Explain**: "Encapsulation protects data. Private attributes (with `_`) can only be changed through methods."

```python
# Show this code:
class User:
    def __init__(self, name: str, user_id: int):
        self._borrowed_books: list = []  # Private!

    def borrow_book(self, book: Book):
        book.borrow()  # Checks if available
        self._borrowed_books.append(book)  # Adds safely

    def get_borrowed(self) -> list:
        return list(self._borrowed_books)  # Returns copy, not reference
```

**Say**: "Users can't directly modify `_borrowed_books`. They must use `borrow_book()`, which checks availability first. This prevents bugs like borrowing the same can book twice."

**Demo**: "If someone tries `user._borrowed_books.append(book)` directly, it works in Python but violates our contract. In real projects, this would be caught in code review."

---

## Part 3: Design Pattern Demonstration (2 minutes)

### Factory Pattern

**Explain**: "When loading from JSON, we don't know if a book is Physical or eBook. The Factory pattern solves this."

```python
# Show this code:
@staticmethod
def from_dict(data: dict) -> "Book":
    if data["type"] == "physical":
        return PhysicalBook(data["title"], ...)
    elif data["type"] == "ebook":
        return EBook(data["title"], ...)
    else:
        raise ValueError("Unknown type")

# Usage:
book_data = {"type": "physical", "title": "Clean Code", ...}
book = Book.from_dict(book_data)  # Returns correct type!
```

**Say**: "Instead of `if type == physical: book = PhysicalBook(...)`, we centralize creation logic. When we add a new book type, only THIS function changes. All deserialization code stays the same."

---

## Part 4: Unit Tests Demonstration (3 minutes)

### Run Tests

```bash
python -m pytest test_library.py -v
```

**Show output**: 14 tests passing

**Explain each test type**:

#### Test Category 1: Borrowing Logic (5 tests)

```python
def test_borrow_book(self):
    """Validates encapsulation: borrowing changes state correctly"""
    self.assertTrue(book.is_available)
    user.borrow_book(book)
    self.assertFalse(book.is_available)  # State changed
    self.assertIn(book, user.get_borrowed())  # Correctly tracked
```

#### Test Category 2: Fine Calculation (5 tests)

```python
def test_fine_calculation_overdue(self):
    """Validates loan tracking and business logic"""
    due_date = date.today() - timedelta(days=5)  # 5 days overdue
    loan = Loan(..., due_date=due_date)
    fine = calculate_fine(loan)
    self.assertGreater(fine, 0)  # Fee applies
```

#### Test Category 3: Integration (4 tests)

```python
def test_librarian_lend_book(self):
    """Validates Librarian separates concerns from Library"""
    librarian.lend_book(user, book)  # Librarian operation
    self.assertIn(book, user.get_borrowed())  # Reflected in user
```

**Say**: "We have 14 tests covering core functionality. Each test validates one behavior, making it easy to catch regressions."

---

## Part 5: Live Demo (3-4 minutes)

### Run the Demo

```bash
python main.py
```

**Narrate during execution**:

1. **"Creating library"** — Shows abstraction (different book types treated the same)
2. **"Registering members"** — Shows encapsulation (member list protected)
3. **"Borrowing books"** — Shows polymorphism (different display for physical vs eBook)
4. **"Calculating fines"** — Shows business logic (days overdue → fine amount)
5. **"Saving to JSON"** — Shows serialization (using Factory pattern)
6. **"Reloading from file"** — Shows deserialization (Factory creates correct types)

---

## Part 6: Design Decisions & Trade-offs (2 minutes)

### Decision 1: Abstract Book vs Concrete BookType

**Decision**: Use abstract Book class
**Why**: Different types (Physical, eBook) have uniquely different attributes
**Trade-off**: Slightly more code, but much better extensibility

### Decision 2: Separate Librarian Class

**Decision**: Don't put librarian operations in Library
**Why**: Clear separation - Library is data layer, Librarian is business logic layer
**If challenged**: "If we add new roles (Admin, Patron), each gets its own class. Library stays simple."

### Decision 3: Factory Pattern in Book Class

**Decision**: Put factory method in Book class, not separate factory class
**Why**: For small projects, grouping related functionality is better than over-engineering
**If challenged**: "When the project grows, we can extract to BookFactory. Now, it's simpler."

### Decision 4: Dataclass for Loan

**Decision**: Use @dataclass instead of full class
**Why**: Loan is simple data container - avoids boilerplate
**If challenged**: "We get automatic **init**, _eq_, and serialization support for free."

---

## Part 7: Addressing Potential Questions

### Q: "Why not use a default dict for users instead of User class?"

**A**: "That would lose encapsulation. A User class ensures we can't accidentally create a user with invalid ID, and methods like `get_borrowed()` can return a copy (preventing external modifications)."

### Q: "Could you simplify by removing Librarian?"

**A**: "Technically yes, but then Library would do both data management AND business logic. This violates Single Responsibility Principle. If you need to change member management logic later, it's isolated to Librarian."

### Q: "Why @dataclass for Loan instead of a full class?"

**A**: "Loan is a simple data container with just properties and two methods. @dataclass eliminates 10 lines of boilerplate **init** and **repr** while providing serialization support."

### Q: "How would you extend this project?"

**A**:

- Add AudioBook type (implement abstract methods, add to factory)
- Add Reservation system (new class, Librarian gets manage_reservation() method)
- Add payment integration (new fine tracking strategy)
- Add book ratings (add to Book class)

---

## Part 8: Summary Slide

### "We've demonstrated:"

✅ **All 4 OOP Pillars**

- Abstraction: Book abstract class
- Inheritance: PhysicalBook, EBook extend Book
- Polymorphism: Different get_info() per type
- Encapsulation: Private attributes, controlled access

✅ **Design Pattern**

- Factory: Book.from_dict() for type-agnostic creation

✅ **Unit Tests**

- 14 tests covering borrowing, fines, integration

✅ **Complete Project**

- All features working
- Persistence implemented
- No half-finished features

---

## Part 9: Closing Statement

"This project demonstrates that good OOP design is about making code easier to understand, maintain, and extend. Every pillar and pattern serves a purpose—reducing duplication, protecting data, and enabling safe changes. In real projects, these become increasingly valuable as codebases grow."

---

## Timing Guide

- Overview: 2-3 min
- OOP Pillars: 4-5 min
- Design Pattern: 2 min
- Unit Tests: 3 min
- Live Demo: 3-4 min
- Design Decisions: 2 min
- Q&A: 2-3 min

**Total: ~20-25 minutes** (fits typical presentation window)
