from datetime import date
from models.book import PhysicalBook, EBook
from models.user import User
from models.library import Library
from models.librarian import Librarian

# Create library
lib = Library("Narva City Library")
lib.add_book(PhysicalBook("Clean code", "Robert Martin", 2008, 464))
lib.add_book(EBook("Design patterns", "Group of four", 1994, 12.5))
lib.add_book(PhysicalBook("Learning Python", "Mark Lutz", 2019, 1200))

# Create librarian
librarian = Librarian("John", lib)

# Create and register users
alice = User("Alice", user_id=1)
bob = User("Bob", user_id=2)
librarian.register_member(alice)
librarian.register_member(bob)

# Borrow books through librarian
print("\n--- Borrowing books ---")
available = librarian.get_available_books()
if available:
    librarian.lend_book(alice, available[0])

lib.show_all()

print("\n--- Returning a book ---")
book = alice.get_borrowed()[0]
alice.return_book(book)

lib.show_all()
lib.save()

print("\n--- Reload from file ---")
lib2 = Library.load("library_data.json")
lib2.show_all()
