from django.shortcuts import render

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

# ListView: Retrieve all books (read-only for everyone)
class BookListView(generics.ListAPIView):
    """
    View to list all books.
    Accessible to all users (authenticated or not).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# DetailView: Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a specific book by primary key.
    Public read-only access.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# CreateView: Add a new book (only for authenticated users)
class BookCreateView(generics.CreateAPIView):
    """
    View to create a new book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# UpdateView: Modify an existing book
class BookUpdateView(generics.UpdateAPIView):
    """
    View to update an existing book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# DeleteView: Remove a book
class BookDeleteView(generics.DestroyAPIView):
    """
    View to delete a book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]