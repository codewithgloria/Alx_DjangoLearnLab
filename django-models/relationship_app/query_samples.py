"""
query_samples.py

Sample ORM queries for:
1. All books by a specific author
2. All books in a library
3. Librarian for a library
"""

from relationship_app.models import Author, Book, Library, Librarian


def query_all_books_by_author(author_name):
    """Get all books written by a specific author."""
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()
        print(f"\nBooks by {author_name}:")
        for book in books:
            print(f" - {book.title}")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")


def list_all_books_in_library(library_name):
    """List all books in a specific library."""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"\nBooks in {library_name}:")
        for book in books:
            print(f" - {book.title}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")


def retrieve_librarian_for_library(library_name):
    """Retrieve the librarian for a specific library."""
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian
        print(f"\nLibrarian for {library_name}: {librarian.name}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library_name}.")


# Example usage (uncomment to test after creating data)
# if __name__ == "__main__":
#     query_all_books_by_author("George Orwell")
#     list_all_books_in_library("Central Library")
#     retrieve_librarian_for_library("Central Library")