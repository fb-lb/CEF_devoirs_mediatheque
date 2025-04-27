from django.shortcuts import render
from librarians_app.models import Book, Cd, Dvd, ParlourGame

def medias_list(request):
    books = Book.objects.all()
    cds = Cd.objects.all()
    dvds = Dvd.objects.all()
    parlour_games = ParlourGame.objects.all()
    return render(request, 'mediasList.html', {
        'books': books,
        'cds': cds,
        'dvds': dvds,
        'parlour_games': parlour_games
    })