from django.db import models

from django.db import models
from datetime import date

class Author(models.Model):
    """
    Model representing an author.
    Each author can have multiple books (one-to-many relationship).
    """
    name = models.CharField(max_length=100, help_text="Enter the author's full name")

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Model representing a book.
    Linked to an Author via ForeignKey.
    """
    title = models.CharField(max_length=200, help_text="Enter the book's title")
    publication_year = models.IntegerField(help_text="Year the book was published")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title