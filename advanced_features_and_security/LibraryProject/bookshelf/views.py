from .forms import ExampleForm
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from relationship_app.models import Book

@permission_required('relationship_app.can_view', raise_exception=True)
def book_list(request):
    """View to list all books - requires can_view permission."""
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# secure search view
def search_books(request):
    query = request.GET.get('q', '').strip()
    books = []
    if query:
        #
        books = Book.objects.filter(title__icontains=query)
    return render(request, 'bookshelf/book_list.html', {'books': books})

def example_form_view(request):
    form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})