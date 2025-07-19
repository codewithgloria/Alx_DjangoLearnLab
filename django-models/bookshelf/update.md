## Update Operation

Command:
```python
book.title = "Nineteen Eighty-Four"
book.save()

updated_book = Book.objects.get(title="Nineteen Eighty-Four")
print(updated_book.title)