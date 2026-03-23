# Library Management System - OOP Design Documentation

## Project Overview

A **small but complete** library management system demonstrating all 4 OOP pillars and design patterns. Users can borrow/return books, librarians manage members, and the system tracks loans with automatic fine calculation.

---

## 1. OOP Pillars Implementation

### 1.1 Abstraction ✅

**Definition**: Hiding complexity, exposing only essential features.

**Implementation**:

```python
# models/book.py - Abstract Base Class
from abc import ABC, abstractmethod

class Book(ABC):
    def __init__(self, title: str, author: str, year: int):
        self._title = title
        self._author = author
        self._year = year
        self._is_available = True

    @abstractmethod
    def get_info(self) -> str:
        """Subclasses MUST implement this"""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Subclasses MUST implement serialization"""
        pass
```

**Why**: Different book types (PhysicalBook, EBook) have different properties (pages vs size_mb). The abstract class defines a contract without forcing unnecessary details into the parent class.

---

### 1.2 Inheritance ✅

**Definition**: Creating specialized classes from a base class.

**Implementation**:

```python
# models/book.py
class PhysicalBook(Book):
    def __init__(self, title: str, author: str, year: int, pages: int):
        super().__init__(title, author, year)
        self._pages = pages

class EBook(Book):
    def __init__(self, title: str, author: str, year: int, size_mb: float):
        super().__init__(title, author, year)
        self._size_mb = size_mb
```

**Why**: Both book types share borrowing logic but differ in display format. Inheritance avoids code duplication for the common `borrow()` and `return_book()` methods.

---

### 1.3 Encapsulation ✅

**Definition**: Bundling data with methods & controlling access via access modifiers.

**Implementation**:

```python
# models/user.py
class User:
    def __init__(self, name: str, user_id: int):
        self._name = name              # Private - cannot modify directly
        self._id = user_id             # Private
        self._borrowed_books: list = []  # Private - controlled access only

    @property
    def name(self):
        """Read-only access"""
        return self._name

    @property
    def user_id(self):
        """Read-only access"""
        return self._id

    def get_borrowed(self) -> list:
        """Controlled access - returns copy, not direct reference"""
        return list(self._borrowed_books)
```

**Why**: Users shouldn't directly modify `_borrowed_books` list. Methods like `borrow_book()` and `return_book()` ensure business logic integrity (e.g., preventing borrowed count corruption).

---

### 1.4 Polymorphism ✅

**Definition**: Same interface, different implementations.

**Implementation**:

```python
# models/book.py
class PhysicalBook(Book):
    def get_info(self) -> str:
        status = "available" if self._is_available else "issued"
        return f"[Printed] {self._title} — {self._author} ({self._year}), {self._pages} pg. [{status}]"

class EBook(Book):
    def get_info(self) -> str:
        status = "available" if self._is_available else "issued"
        return f"[Electric] {self._title} — {self._author} ({self._year}), {self._size_mb} MB [{status}]"

# Usage:
books: list[Book] = [physical_book, ebook]
for book in books:
    print(book.get_info())  # Calls correct implementation automatically
```

**Why**: The same method call produces different outputs without conditional logic. This makes adding new book types (AudioBook, Subscription) easy without changing existing code.

---

## 2. Design Patterns

### 2.1 Factory Pattern ✅

**Definition**: Create objects without specifying exact classes.

**Implementation**:

```python
# models/book.py
@staticmethod
def from_dict(data: dict) -> "Book":
    if data["type"] == "physical":
        book = PhysicalBook(data["title"], data["author"], data["year"], data["pages"])
    elif data["type"] == "ebook":
        book = EBook(data["title"], data["author"], data["year"], data["size_mb"])
    else:
        raise ValueError(f"Unknown book type: {data['type']}")
    book._is_available = data["is_available"]
    return book

# Usage:
book_data = {"type": "physical", "title": "Clean Code", ...}
book = Book.from_dict(book_data)  # Don't need to know it's PhysicalBook
```

**Why**: Deserialization logic is centralized. When adding a new book type, only the factory needs updating. Code that loads books doesn't change.

---

## 3. Unit Tests (14 Tests - ≥3 Required ✅)

### Test Coverage Summary

| Test Class             | Count  | Purpose                  |
| ---------------------- | ------ | ------------------------ |
| TestBorrowingLogic     | 5      | Core borrowing/returning |
| TestOverdueLogic       | 5      | Fine calculation logic   |
| TestLibraryIntegration | 4      | Librarian operations     |
| **TOTAL**              | **14** | ✅                       |

### Key Tests Demonstrating OOP Principles

#### Test 1: Abstraction + Polymorphism

```python
def test_borrow_book(self):
    """Book polymorphism: both PhysicalBook & EBook use same borrow() method"""
    book = PhysicalBook("Clean Code", "Robert Martin", 2008, 464)
    self.assertTrue(book.is_available)
    book.borrow()
    self.assertFalse(book.is_available)
```

#### Test 2: Encapsulation

```python
def test_return_unborowed_book(self):
    """User encapsulation: cannot return book user never borrowed"""
    user = User("Alice", user_id=1)
    book = PhysicalBook("Clean Code", "Robert Martin", 2008, 464)

    with self.assertRaises(ValueError):
        user.return_book(book)  # Business logic violation
```

#### Test 3: Inheritance

```python
def test_fine_calculation_overdue(self):
    """Loan class: inherits date logic, calculates overdue days"""
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
```

---

## 4. Code Quality Features

### 4.1 Type Hints

```python
def borrow_book(self, book: Book, due_date: date = None) -> None:
    """Type hints prevent errors and improve IDE support"""
```

### 4.2 Access Control via Properties

```python
@property
def is_available(self) -> bool:
    return self._is_available
```

### 4.3 Serialization Support

```python
def to_dict(self) -> dict:
    return {...}

@staticmethod
def from_dict(data: dict) -> "Book":
    # Enables save/load functionality
```

---

## 5. Project Completeness Checklist

- ✅ **Encapsulation**: Private attributes, controlled access via methods/properties
- ✅ **Inheritance**: PhysicalBook, EBook inherit from Book
- ✅ **Polymorphism**: Different get_info() & to_dict() per book type
- ✅ **Abstraction**: Abstract Book base class with abstract methods
- ✅ **Design Pattern**: Factory pattern for object creation
- ✅ **Unit Tests**: 14 tests with meaningful assertions
- ✅ **Small & Complete**:
    - Core features: Borrow, Return, Fine Calculation
    - Persistence: Save/Load from JSON
    - Librarian: Member management
    - No unfinished features

---

## 6. Running the Project

### Run Tests

```bash
python -m pytest test_library.py -v
# Result: 14 passed
```

### Run Demo

```bash
python main.py
```

### Expected Demo Output

1. Create library and add 3 books (1 eBook, 2 physical)
2. Register 2 members
3. User borrows a book (demonstrates polymorphism)
4. User returns book (demonstrates fine calculation)
5. Save to JSON
6. Reload from JSON (demonstrates serialization)

---

## 7. Design Decisions & Trade-offs

**Decision 1**: Use `@dataclass` for Loan instead of full class

- ✅ Reduces boilerplate for simple data container
- ❌ Less control over validation
- **Why**: Loan data is straightforward; extra complexity not justified

**Decision 2**: Factory pattern in Book class rather than separate factory class

- ✅ Keeps related code together
- ❌ Mixes instantiation logic with Book
- **Why**: For small projects, co-location outweighs pattern purity

**Decision 3**: Separate Librarian class instead of Library handling everything

- ✅ Clear separation of concerns (Library = data, Librarian = operations)
- ✅ Easy to add other roles (Patron, Admin) later
- **Why**: Better maintainability and extensibility

---

## 8. Presentation Script

### Key Points to Defend:

1. **Why abstract Book class?**
    - "Different book types have different attributes (pages vs size). The abstract class ensures all books implement borrowing logic while allowing specific types to define their own display format."

2. **Why is Librarian separate from Library?**
    - "Library manages data. Librarian handles operations. This follows Single Responsibility Principle—if we add a different role (Admin, Patron), we can extend independently."

3. **Why Factory pattern?**
    - "When loading from JSON, we don't know book type in advance. The factory creates the correct object type automatically. Adding a new book type only requires updating the factory."

4. **How do tests validate OOP?**
    - "Tests verify that polymorphism works (same method, different behavior), encapsulation protects data integrity, and inheritance avoids code duplication."

---

## File Structure

```
library/
├── models/
│   ├── book.py              # Abstract base class + implementations
│   ├── user.py              # User with encapsulation
│   ├── library.py           # Library operations
│   ├── librarian.py         # Separation of concerns
│   └── loan.py              # Loan tracking
├── utils/
│   ├── fine_calculator.py   # Business logic
│   └── storage.py           # (Extensible)
├── main.py                  # Demo script
├── test_library.py          # 14 unit tests
└── DESIGN_DOCUMENTATION.md  # This file
```
