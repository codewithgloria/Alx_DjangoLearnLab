## Retrieve Operation

Command:
```python
book = Book.objects.get(title="1984")
print(book.title)
print(book.author)
print(book.publication_year)