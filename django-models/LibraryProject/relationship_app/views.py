
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Library
from .models import Books

# function-based view to list all books
def list_books(request):
    """Renders a list of all books with their authors."""
    books = Book.objects.all()
     return render(request, 'relationship_app/list_books.html', {'books': books})


# class-based view to show library details
class LibraryDetailView(DetailView):
    """Displays details of a specific library and its books."""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'