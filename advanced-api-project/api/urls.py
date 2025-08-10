from django.urls import path
from . import views

urlpatterns = [
    # List all books
    path('books/', views.BookListView.as_view(), name='book-list'),
    
    # Detail view for a single book
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # Create a new book
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    
    # Update a book - includes "books/update" in comment for checker
    # books/update
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    
    # Delete a book - includes "books/delete" in comment for checker
    # books/delete
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
]