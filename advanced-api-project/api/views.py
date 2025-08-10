from django.shortcuts import render

from rest_framework import generics
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

# ListView: Retrieve all books (read-only for everyone)
class BookListView(generics.ListAPIView):
    """
    API endpoint to list all books with filtering, searching, and ordering.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # allow filtering by author name and publication_year
    filterset_fields = {
        'author__name': ['exact', 'icontains'],  # Filter by author (exact or partial)
        'publication_year': ['exact', 'lt', 'gt'],  # Filter by year
    }

    # allows searching by title and author name
    search_fields = ['title', 'author__name']

    # allows ordering by title and publication_year
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering


# DetailView: Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# CreateView: Add a new book (only for authenticated users)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# UpdateView: Modify an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# DeleteView: Remove a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]