from relationship_app.models import Author, Book, Library, Librarian

def query_samples():
    # querying all books by a specific author
    author = Author.objects.get(name="George Orwell")
    books_by_author = Book.objects.filter(author=author)
    print(f"Books by {author.name}:")
    for book in books_by_author:
        print(f" - {book.title}")

    # listing all books in a library
    library = Library.objects.get(name="Central Library")
    books_in_library = library.books.all()
    print(f"\nBooks in {library.name}:")
    for book in books_in_library:
        print(f" - {book.title}")

    # retrieving the librarian for a library
    librarian = Librarian.objects.get(library__name="Central Library")
    print(f"\nLibrarian for {librarian.library.name}: {librarian.name}")

if __name__ == "__main__":
    query_samples()