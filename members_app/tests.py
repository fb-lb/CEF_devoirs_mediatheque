import pytest
from django.urls import reverse
from librarians_app.models import Book, ParlourGame


@pytest.mark.django_db
def test_medias_list(client):
    url = reverse('medias_list')
    Book.objects.create(name='Livre test', author='Auteur test')
    ParlourGame.objects.create(name='Jeu test', creator='Créateur test')
    response = client.get(url)

    assert response.status_code == 200
    assert b"Livre test" in response.content
    assert b"Jeu test" in response.content