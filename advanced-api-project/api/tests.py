from django.test import TestCase

# api/tests.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book

# Get the custom or default User model
User = get_user_model()

class BookAPITests(APITestCase):
    """
    Test suite for Book API endpoints.
    Tests CRUD operations, filtering, searching, ordering, and permissions.
    """

    def setUp(self):
        # Create test user for authenticated endpoints
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Create an author
        self.author = Author.objects.create(name="George Orwell")

        # Create a book
        self.book = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author
        )

        # Define URLs
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book.pk})
        self.create_url = reverse('book-create')
        self.update_url = reverse('book-update', kwargs={'pk': self.book.pk})
        self.delete_url = reverse('book-delete', kwargs={'pk': self.book.pk})

    # ✅ Test 1: Can retrieve list of books (GET)
    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "1984")

    # ✅ Test 2: Can retrieve a single book detail (GET)
    def test_retrieve_book_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['author'], self.author.id)
        self.assertEqual(response.data['title'], "1984")

    # ✅ Test 3: Can create a new book (POST) - authenticated only
    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            "title": "Animal Farm",
            "publication_year": 1945,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    # ✅ Test 4: Cannot create book if unauthenticated
    def test_create_book_unauthenticated(self):
        data = {
            "title": "Animal Farm",
            "publication_year": 1945,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ✅ Test 5: Can update a book (PUT/PATCH) - authenticated only
    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        updated_data = {
            "title": "Nineteen Eighty-Four",
            "publication_year": 1949,
            "author": self.author.id
        }
        response = self.client.put(self.update_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Nineteen Eighty-Four")

    # ✅ Test 6: Cannot update if unauthenticated
    def test_update_book_unauthenticated(self):
        updated_data = {
            "title": "Nineteen Eighty-Four",
            "publication_year": 1949,
            "author": self.author.id
        }
        response = self.client.put(self.update_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ✅ Test 7: Can delete a book (DELETE) - authenticated only
    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    # ✅ Test 8: Cannot delete if unauthenticated
    def test_delete_book_unauthenticated(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ✅ Test 9: Filtering by author name
    def test_filter_books_by_author(self):
        response = self.client.get(self.list_url, {'author__name': 'George'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "1984")

    # ✅ Test 10: Search functionality
    def test_search_books(self):
        response = self.client.get(self.list_url, {'search': '1984'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # ✅ Test 11: Ordering functionality
    def test_ordering_books(self):
        # Create another book
        Book.objects.create(
            title="Animal Farm",
            publication_year=1945,
            author=self.author
        )
        response = self.client.get(self.list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))  # Should be in alphabetical order

    # ✅ Test 12: Publication year cannot be in the future (validation)
    def test_create_book_future_year(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            "title": "Future Book",
            "publication_year": 2030,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Publication year cannot be in the future", str(response.data))