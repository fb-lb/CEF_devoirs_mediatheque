import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from librarians_app.models import Book, Member, Dvd
from datetime import timedelta


@pytest.mark.django_db
def test_login_view(client):
    # Test getting login page
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    assert b"Connexion" and b"Nom d'utilisateur" and b"Mot de passe" in response.content

    # Test of connexion with valid username and password
    user = User.objects.create_user(username='testunsername', password='testpassword')
    response = client.post(url, {
        'username': 'testunsername',
        'password': 'testpassword'
    })
    assert response.status_code == 302
    assert response.url == '/'

    # Test of connexion with invalid username and password
    response = client.post(url, {
        'username': 'invalidunsername',
        'password': 'invalidpassword'
    })
    assert response.status_code == 200
    assert b"Nom d'utilisateur ou mot de passe incorrect." in response.content

@pytest.mark.django_db
def test_logout(client):
    # Creation of a valid login
    user = User.objects.create_user(username='testusername', password='testpassword')
    client.login(username='testusername', password='testpassword')

    # Test of a logout
    response = client.post(reverse('logout'))
    assert response.status_code == 302
    assert response.url == '/bibliothecaire/connexion/'

@pytest.mark.django_db
def test_create_medias(client):
    # Creation of a valid login
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')

    # Test new media creation
    url = reverse('media_management')
    response = client.post(url, {
        'submit_create_media': 'Enregistrer',
        'media_type': 'book',
        'name': 'Livre Test',
        'author': 'Auteur Test'
    })
    book = Book.objects.get(name='Livre Test')
    assert response.status_code == 302
    assert book.author == 'Auteur Test'

@pytest.mark.django_db
def test_delete_medias(client):
    # Connexion of librarian and creation of a book
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    book = Book.objects.create(name='Livre test', author='Auteur test')

    # Test delete media form
    url = reverse('media_management')
    response = client.post(url, {
        'submit_delete_media': 'Supprimer',
        'media_type': 'media',
        'id': book.id
    })
    assert response.status_code == 302
    assert not Book.objects.filter(pk=book.id).exists()

@pytest.mark.django_db
def test_update_medias(client):
    # Connexion of librarian and creation of a book
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    book = Book.objects.create(name='Livre test', author='Auteur test')

    # Test update media form
    url = reverse('media_management')
    response = client.post(url, {
        'submit_update_media': 'Modifier',
        'media_type': 'media',
        'name': 'Livre test modifié',
        'author': 'Auteur test',
        'id': book.id
    })
    update_book = Book.objects.get(pk=book.id)
    assert response.status_code == 302
    assert update_book.name == 'Livre test modifié'

@pytest.mark.django_db
def test_create_member(client):
    # Creation of a valid login
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')

    # Test new member creation
    url = reverse('members_management')
    response = client.post(url, {
        'submit_create_member': 'Enregistrer',
        'first_name': 'Prénom Membre',
        'last_name': 'Nom Membre'
    })

    member = Member.objects.get(first_name='Prénom Membre')
    assert response.status_code == 302
    assert member.last_name == 'Nom Membre'

@pytest.mark.django_db
def test_delete_member(client):
    # Connexion of librarian and creation of a member
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    member = Member.objects.create(first_name='Prénom Membre', last_name='Nom Membre')

    # Test on delete member form
    url = reverse('members_management')
    response = client.post(url, {
        'submit_delete_member': 'Supprimer',
        'id': member.id
    })
    assert response.status_code == 302
    assert not Member.objects.filter(pk=member.id).exists()

@pytest.mark.django_db
def test_update_member(client):
    # Connexion of librarian and creation of a member
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    member = Member.objects.create(first_name='Prénom Membre', last_name='Nom Membre')

    # Test on update member form
    url = reverse('members_management')
    response = client.post(url, {
        'submit_update_member': 'Modifier',
        'id': member.id,
        'last_name': 'Nom Membre',
        'first_name': 'Prénom Membre Modifié',
        'is_blocked': 'false'
    })
    update_member = Member.objects.get(pk=member.id)
    assert response.status_code == 302
    assert update_member.first_name == 'Prénom Membre Modifié'

@pytest.mark.django_db
def test_new_borrowing(client):
    # Connexion of librarian and creation of a member, a book and a dvd
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    member = Member.objects.create(first_name='Prénom Membre', last_name='Nom Membre')
    book = Book.objects.create(name='Livre test', author='Auteur test')
    dvd = Dvd.objects.create(name='DVD test', director='Réalisateur test')
    assert book.is_available == True
    assert book.borrower is None

    # Test of a valid new borrowing creation
    response = client.post(reverse('borrowings'), {
        'submit_borrowing': "Enregistrer l'emprunt",
        'media_id': book.id,
        'member_id': member.id
    })
    book_borrowed = Book.objects.get(pk=book.id)
    assert response.status_code == 302
    assert book_borrowed.borrower == member
    assert book_borrowed.is_available == False

    # Update member's number of borrowing at 3
    member.nb_current_borrowings = 3
    member.save()

    # Test that member who have 3 currents borrowings can't have a new one
    response = client.post(reverse('borrowings'), {
        'submit_borrowing': "Enregistrer l'emprunt",
        'media_id': dvd.id,
        'member_id': member.id
    }, follow=True)
    dvd_no_borrowed = Dvd.objects.get(pk=dvd.id)
    assert response.status_code == 200
    assert "Ce membre ne peut pas emprunter car il a déjà 3 emprunts à son nom" in response.content.decode()
    assert dvd_no_borrowed.borrower is None
    assert dvd_no_borrowed.is_available == True

    # Update member's number of borrowing at 1
    member.nb_current_borrowings = 1
    member.save()

    # Update return date to block member
    book_borrowed.return_date -= timedelta(days=8)
    book_borrowed.save()

    # Test at the time that late member is blocked and can't have a new borrowing
    response = client.post(reverse('borrowings'), {
        'submit_borrowing': "Enregistrer l'emprunt",
        'media_id': dvd.id,
        'member_id': member.id
    }, follow=True)
    member_blocked = Member.objects.get(pk=member.id)
    assert response.status_code == 200
    assert b"Ce membre ne peut pas emprunter car il est interdit d'emprunt" in response.content
    assert member_blocked.is_blocked == True
    assert dvd_no_borrowed.borrower is None
    assert dvd_no_borrowed.is_available == True

@pytest.mark.django_db
def test_return_borrowing(client):
    # Connexion of librarian and creation of a member and a book and a new borrowing
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    member = Member.objects.create(first_name='Prénom Membre', last_name='Nom Membre')
    book = Book.objects.create(name='Livre test', author='Auteur test')
    client.post(reverse('borrowings'), {
        'submit_borrowing': "Enregistrer l'emprunt",
        'media_id': book.id,
        'member_id': member.id
    })
    book_borrowed = Book.objects.get(pk=book.id)
    assert book_borrowed.borrower == member
    assert book_borrowed.is_available == False

    # Test of borrowing return
    response = client.post(reverse('borrowings'), {
        'submit_return': 'Enregistrer le retour',
        'member_id': member.id,
        'media_id': book_borrowed.id
    })
    book_returned = Book.objects.get(pk=book.id)
    assert response.status_code == 302
    assert book_returned.borrower is None
    assert book_returned.is_available == True