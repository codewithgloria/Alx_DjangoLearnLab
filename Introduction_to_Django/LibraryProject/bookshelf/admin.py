from django.contrib import admin
from bookshelf.models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # this displays fields in list view
    list_display = ('title', 'author', 'publication_year')
    
    # this adds filter sidebar for publication_year
    list_filter = ('publication_year',)
    
    # this enables search for title and author
    search_fields = ('title', 'author')