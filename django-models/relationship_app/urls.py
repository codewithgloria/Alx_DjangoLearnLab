from django.urls import path
from . import views

urlpatterns = [
    # Function-based view: List all books
    path('books/', views.list_books, name='list_books'),

    # Class-based view: Detail of a specific library
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]