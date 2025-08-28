from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required 

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

def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect('list_books')  # Redirect to book list
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})