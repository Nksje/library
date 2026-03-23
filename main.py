from datetime import date
from models.book import PhysicalBook, EBook
from models.user import User
from models.library import Library

lib = Library("Narva City Library")
lib.add_book(PhysicalBook("Clean code", "Robert Martin", 2008, 464))
lib.add_book(EBook("Design patterns", "Group of four", 1994, 12.5))
lib.add_book(PhysicalBook("Learning Python", "Mark Lutz", 2019, 1200))

alice = User("Alice", user_id=1)
book = lib.available_books()[0]
alice.borrow_book(book, due_date=date(2026, 3, 13))

lib.show_all()

print("\n--- Returning a book ---")
alice.return_book(book)

lib.show_all()
lib.save()

print("\n--- Reload from file ---")
lib2 = Library.load("library_data.json")
lib2.show_all()
