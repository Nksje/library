# Library Management System - OOP Python Project

**A complete OOP project demonstrating all 4 programming pillars, SOLID-oriented layering, design patterns, and comprehensive unit testing.**

---

## 📋 Project Summary

A library management system where:

- ✅ Users can borrow and return two types of books (physical & eBooks)
- ✅ System automatically calculates late fees based on return date
- ✅ Librarians manage member registrations and book lending
- ✅ Data persists to JSON file and loads on restart

**Lines of Code**: ~450 (small & complete)  
**Test Coverage**: 14 unit tests (> 3 required)  
**Design Patterns**: 1 (Factory Pattern)  
**OOP Pillars**: All 4 (Abstraction, Inheritance, Polymorphism, Encapsulation)  
**SOLID**: Applied in catalog/persistence/fine-policy boundaries (see below)

---

## 🚀 Quick Start

### Run the Demo

```bash
python main.py
```

Expected output:

```
The book is added: Clean code
The book is added: Design patterns
The book is added: Learning Python
📋 Member registered: Alice
📋 Member registered: Bob

--- Borrowing books ---
Alice took the book: Clean code (due date: 2026-04-06)
Library: Narva City Library
 • [Printed] Clean code — Robert Martin (2008), 464 pg. [issued]
 • [Electric] Design patterns — Group of four (1994), 12.5 MB [available]
 • [Printed] Learning Python — Mark Lutz (2019), 1200 pg. [available]

--- Returning a book ---
Alice returned the book: Clean code
...
💾 Saved 3 of books → library_data.json
📂 Loaded 3 of books from library_data.json
```

### Run Tests

With pytest (if installed):

```bash
python -m pytest test_library.py -v
```

With the standard library only:

```bash
python -m unittest test_library.py -v
```

Expected result: **14 tests**, all passing.

---

## 📂 Project Structure

```
library/
├── abstractions/                # Protocols (DIP / ISP)
│   ├── __init__.py
│   └── protocols.py            # LibraryCatalog, LibraryPersistence, FinePolicy
├── models/                      # Core domain classes
│   ├── __init__.py
│   ├── book.py                 # ⭐ Abstract Book + implementations + factory
│   ├── user.py                 # User with encapsulation + injectable fine policy
│   ├── library.py              # Catalog + orchestrated persistence
│   ├── librarian.py            # Staff operations against LibraryCatalog
│   └── loan.py                 # Loan tracking (dataclass)
├── services/                    # Infrastructure (SRP)
│   ├── __init__.py
│   └── json_library_persistence.py  # JSON save/load only
├── utils/
│   └── fine_calculator.py      # Fine policy + helpers
├── main.py                      # ⭐ Demo script
├── test_library.py             # ⭐ 14 unit tests
├── library_data.json           # Persisted library data
├── DESIGN_DOCUMENTATION.md     # ⭐ How OOP concepts work
├── PRESENTATION_SCRIPT.md      # ⭐ Talking points & defence
├── QUICK_REFERENCE.md          # ⭐ Code location guide
└── README.md                   # This file
```

---

## 🏗️ OOP Pillars Implementation

### 1. **Abstraction** — Hiding Complexity

**Location**: `models/book.py` (Lines 1-20)

Abstract base class defines WHAT all books do (borrowing logic) without specifying HOW different types display themselves.

```python
from abc import ABC, abstractmethod

class Book(ABC):
    @abstractmethod
    def get_info(self) -> str:
        """Each subclass implements display differently"""
        pass
```

**Why**: Physical books and eBooks display differently but share borrowing logic.

---

### 2. **Inheritance** — Code Reuse

**Location**: `models/book.py` (Lines 45-75)

PhysicalBook and EBook inherit from Book, reusing `borrow()` and `return_book()` methods.

```python
class PhysicalBook(Book):
    def __init__(self, title: str, author: str, year: int, pages: int):
        super().__init__(title, author, year)
        self._pages = pages

class EBook(Book):
    def __init__(self, title: str, author: str, year: int, size_mb: float):
        super().__init__(title, author, year)
        self._size_mb = size_mb
```

**Why**: Avoids duplicating borrowing/returning logic in both classes.

---

### 3. **Polymorphism** — Same Interface, Different Behavior

**Location**: `models/book.py` (Lines 50-75)

Same method `get_info()` produces different outputs automatically.

```python
class PhysicalBook(Book):
    def get_info(self) -> str:
        return f"[Printed] {self._title} — {self._author} ({self._year}), {self._pages} pg."

class EBook(Book):
    def get_info(self) -> str:
        return f"[Electric] {self._title} — {self._author} ({self._year}), {self._size_mb} MB"
```

**Usage**: No if-statements needed

```python
books: list[Book] = [physical_book, ebook]
for book in books:
    print(book.get_info())  # Correct version called automatically
```

**Why**: Easy to add new book types (AudioBook, Subscription) without modifying existing code.

---

### 4. **Encapsulation** — Data Protection

**Location**: `models/user.py` (Lines 1-30)

Private attributes (`_name`, `_borrowed_books`) with controlled access via methods.

```python
class User:
    def __init__(self, name: str, user_id: int):
        self._borrowed_books: list = []  # Private!

    @property
    def name(self):
        return self._name  # Read-only

    def borrow_book(self, book: Book):
        book.borrow()  # Ensures book is available first
        self._borrowed_books.append(book)

    def get_borrowed(self) -> list:
        return list(self._borrowed_books)  # Returns copy
```

**Why**: Prevents bugs like:

- Borrowing a book that's already out
- Corrupting the borrowed list structure
- Orphan books without proper loan tracking

---

## 🧱 SOLID Principles (Where & Why)

| Principle | Meaning (short) | In this project |
|-----------|-----------------|-----------------|
| **S** — Single Responsibility | One class, one reason to change | `JsonLibraryPersistence` only reads/writes JSON; `Library` focuses on the in-memory catalog and delegates I/O; `StandardFinePolicy` holds overdue rules. |
| **O** — Open/Closed | Extend behaviour without editing stable core | New book types extend `Book` + factory (`from_dict` / `to_dict`); new fine rules: implement `FinePolicy` and pass into `User(..., fine_policy=...)` instead of changing `User`. |
| **L** — Liskov Substitution | Subtypes must work wherever the base is expected | Any `Book` subtype can be stored, borrowed, and serialized through the same `Book` interface (`PhysicalBook`, `EBook`). |
| **I** — Interface Segregation | Small, focused interfaces | `LibraryCatalog` exposes only what `Librarian` needs (`find_by_author`, `available_books`), not save/load internals. |
| **D** — Dependency Inversion | Depend on abstractions, not concrete infrastructure | `Library` depends on `LibraryPersistence` (default: `JsonLibraryPersistence`); `Librarian` depends on `LibraryCatalog`; `User` depends on `FinePolicy` (default: `StandardFinePolicy`). |

**Key files**: `abstractions/protocols.py`, `services/json_library_persistence.py`, `models/library.py`, `models/librarian.py`, `models/user.py`, `utils/fine_calculator.py`.

---

## 🎯 Design Pattern: Factory

**Location**: `models/book.py` (Lines 25-42)

Factory pattern creates correct book type from JSON without caller knowing the type.

```python
@staticmethod
def from_dict(data: dict) -> "Book":
    if data["type"] == "physical":
        return PhysicalBook(data["title"], data["author"], data["year"], data["pages"])
    elif data["type"] == "ebook":
        return EBook(data["title"], data["author"], data["year"], data["size_mb"])
    else:
        raise ValueError(f"Unknown book type: {data['type']}")
```

**Benefits**:

- ✅ Deserialization logic centralized
- ✅ Adding new book type only requires updating factory
- ✅ Code that loads books doesn't change
- ✅ Type information implicit in data

---

## 🧪 Unit Tests (14 Total)

### Test Groups

| Group               | Tests  | Purpose                              |
| ------------------- | ------ | ------------------------------------ |
| **Borrowing Logic** | 5      | Core borrow/return functionality     |
| **Overdue & Fines** | 5      | Fine calculation and late tracking   |
| **Integration**     | 4      | Librarian, Library, User cooperation |
| **TOTAL**           | **14** | ✅ All passing                       |

### Test Examples

#### Test 1: Encapsulation Violation Prevention

```python
def test_borrow_unavailable_book(self):
    """Can't borrow book that's already checked out"""
    user1.borrow_book(book)  # First user takes it
    user2 = User("Bob", user_id=2)

    with self.assertRaises(ValueError):
        user2.borrow_book(book)  # Second user can't take it
```

#### Test 2: Polymorphism Verification

```python
def test_borrow_book(self):
    """Both PhysicalBook and EBook use same borrow() method"""
    self.assertTrue(book.is_available)  # Works for all Book types
    book.borrow()  # Polymorphic behavior
    self.assertFalse(book.is_available)
```

#### Test 3: Fine Calculation

```python
def test_fine_calculation_overdue(self):
    """Loan tracking calculates fines correctly"""
    due_date = date.today() - timedelta(days=5)  # 5 days overdue
    loan = Loan(..., due_date=due_date, return_date=date.today())

    fine = calculate_fine(loan)
    self.assertGreater(fine, 0)  # Fine applies
    self.assertLessEqual(fine, 20.0)  # Capped at maximum
```

### Run All Tests

```bash
python -m unittest test_library.py -v
```

(or `python -m pytest test_library.py -v` if pytest is installed)

---

## 📚 How to Present This Project

### Documents Included

1. **[DESIGN_DOCUMENTATION.md](DESIGN_DOCUMENTATION.md)**
    - Detailed explanation of each OOP pillar with code examples
    - Why each design decision was made
    - Trade-offs and reasoning
    - Full file structure overview

2. **[PRESENTATION_SCRIPT.md](PRESENTATION_SCRIPT.md)**
    - Complete talking points for 20-25 minute presentation
    - Suggested code to show at each point
    - Answers to potential questions
    - Live demo narrative

3. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)**
    - File:line locations for each OOP concept
    - Quick tables for navigation
    - How to answer "prove feature X works"
    - Checklist for talking points

### Presentation Flow

1. **Overview** (2-3 min) — What the system does
2. **OOP Pillars** (4-5 min) — Explain each with code examples
3. **SOLID** (2 min) — `LibraryCatalog` / `LibraryPersistence` / `FinePolicy` and their defaults
4. **Design Pattern** (2 min) — Factory pattern benefits
5. **Unit Tests Walkthrough** (3 min) — Show test output
6. **Live Demo** (3-4 min) — Run `main.py`, show JSON persistence
7. **Design Decisions** (2 min) — Trade-offs & reasoning
8. **Q&A** (2-3 min) — Address concerns

**Total**: ~22-28 minutes (adds a short SOLID segment; trim other parts if you must stay at 25 min)

---

## ✨ Key Features

### Core Functionality

- ✅ Add/borrow/return books seamlessly
- ✅ Automatic fine calculation (€0.25/day after grace period)
- ✅ Fine capped at €20.00 maximum
- ✅ Two book types (Physical, eBook) with different properties

### Data Integrity

- ✅ Encapsulation prevents invalid operations
- ✅ Can't borrow unavailable books
- ✅ Can't return books not borrowed
- ✅ Automatic loan tracking

### Persistence

- ✅ Save library to JSON file
- ✅ Load from JSON with correct book types
- ✅ Factory pattern handles deserialization

### Code Quality

- ✅ Type hints throughout
- ✅ Private attributes with `@property` access
- ✅ Comprehensive docstrings
- ✅ Clean separation of concerns
- ✅ SOLID-oriented boundaries (protocols + default adapters)

---

## 🛠️ Project Completeness Checklist

### Requirements

- ✅ All 4 OOP Pillars (Abstraction, Inheritance, Polymorphism, Encapsulation)
- ✅ At least 1 Design Pattern (Factory)
- ✅ Unit Tests (≥3 meaningful) — **14 tests implemented**
- ✅ Small but Complete Scope — All features working, no half-finished features
- ✅ Presentation-Ready — Demo script + design documentation

### Extra Quality Measures

- ✅ Type hints for IDE support
- ✅ Error handling with meaningful messages
- ✅ Clean code following PEP 8
- ✅ Both abstract classes and concrete implementations
- ✅ Dataclass for simple models
- ✅ Property decorators for encapsulation
- ✅ Static factory methods for polymorphic creation
- ✅ Comprehensive test coverage
- ✅ `typing.Protocol` for dependency inversion (catalog, persistence, fines)

---

## 📖 Reading Order for Project Review

1. Start: **README.md** (this file) — Overview
2. Code: **abstractions/protocols.py** — SOLID contracts (catalog, persistence, fines)
3. Code: **models/book.py** — Abstraction + Polymorphism + Factory
4. Code: **models/user.py** — Encapsulation + injectable `FinePolicy`
5. Demo: Run `python main.py` — See it in action
6. Tests: Run `python -m unittest test_library.py -v` — Validate all features
7. Deepen: **DESIGN_DOCUMENTATION.md** — Detailed explanations
8. Present: **PRESENTATION_SCRIPT.md** — Talking points

---

## 🚀 Extending the Project

New features can be added easily due to OOP design:

### Add AudioBook Type

```python
class AudioBook(Book):
    def __init__(self, title: str, author: str, year: int, duration_hours: float):
        super().__init__(title, author, year)
        self._duration_hours = duration_hours

    def get_info(self) -> str:
        return f"[Audio] {self._title} — {self._author}, {self._duration_hours}h"

    def to_dict(self) -> dict:
        return {"type": "audio", "title": self._title, ...}

# Update factory:
elif data["type"] == "audio":
    return AudioBook(...)
```

### Add Reservations

```python
class Reservation:
    def __init__(self, user: User, book: Book, reserved_date: date):
        self.user = user
        self.book = book
        self.reserved_date = reserved_date

# Librarian gets new method:
def reserve_book(self, user: User, book: Book):
    if book.is_available:
        raise ValueError("Can't reserve available books")
    self._reservations.append(Reservation(user, book, date.today()))
```

---

## 📞 Questions? Check:

- **"Where is abstraction?"** → Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) table
- **"How do I defend design decisions?"** → See [PRESENTATION_SCRIPT.md](PRESENTATION_SCRIPT.md) Part 7
- **"Why use factory pattern?"** → See [DESIGN_DOCUMENTATION.md](DESIGN_DOCUMENTATION.md) Section 2.1
- **"Run tests?"** → `python -m unittest test_library.py -v` (or pytest if available)
- **"Where is SOLID?"** → See table above and `abstractions/protocols.py`
- **"Run demo?"** → `python main.py`

---

## 📊 Project Stats

```
Files:           12+ (models, abstractions, services, utils, tests, demo)
Lines of Code:   ~450 (excluding comments)
Test Cases:      14 (all passing ✓)
OOP Pillars:     4/4 implemented
SOLID:           Demonstrated via protocols + focused service classes
Design Patterns: 1/1 implemented (Factory)
Test Pass Rate:  100% (14/14)
Coverage:        Core functionality + edge cases
Documentation:   4 comprehensive guides + this README
```

---

**Ready for presentation!** 🎓

Start with `python main.py` to see it in action, then refer to [PRESENTATION_SCRIPT.md](PRESENTATION_SCRIPT.md) for exact talking points.
