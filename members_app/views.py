from django.shortcuts import render
from librarians_app.models import Book

def books_list(request):
    books = Book.objects.all()
    return render(request, 'booksList.html', {'books': books})