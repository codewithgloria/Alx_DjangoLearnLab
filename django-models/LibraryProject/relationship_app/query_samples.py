from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    # querying all books by a specific author
    author = Author.objects.get(name="author_name")
    books = Book.objects.filter(author=author)
    print(f"Books by {author_name}:")
    for book in books:
        print(f" - {book.title}")
    return books

def query_books_in_library(library_name):
    # listing all books in a library
    library = Library.objects.get(name="library_name")
    books = library.books.all()
    print(f"\nBooks in {library_name}:")
    for book in books:
        print(f" - {book.title}")
    return books

def query_librarian_for_library(library_name):
    # retrieving the librarian for a library
    librarian = Librarian.objects.get(library__name="library_name")
    print(f"\nLibrarian for {library_name}: {librarian.name}")
    return librarian

if __name__ == "__main__":
    #sample names from db
    query_books_by_author("George Orwell")
    query_books_in_library("Central Library")
    query_librarian_for_library("Central Library")