from django.shortcuts import render
from librarians_app.models import BorrowableMedia, ParlourGame

def medias_list(request):
    medias = BorrowableMedia.objects.all()
    for media in medias:
        if hasattr(media, 'book'):
            media.type = media.book.media_type
            media.author = media.book.author
        elif hasattr(media, 'cd'):
            media.type = media.cd.media_type
            media.author = media.cd.artist
        elif hasattr(media, 'dvd'):
            media.type = media.dvd.media_type
            media.author = media.dvd.director
        else:
            media.type = 'Type de média inconnu'
            media.author = 'Média non reconnu'
    parlour_games = ParlourGame.objects.all()
    return render(request, 'mediasList.html', {
        'medias': medias,
        'parlour_games': parlour_games
    })