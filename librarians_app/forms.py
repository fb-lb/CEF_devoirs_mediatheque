from django import forms
from django.contrib.auth.forms import AuthenticationForm

'''
Authentification forms
'''


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur", max_length=150)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


'''
Books management forms
'''
CHOICES_MEDIA_FULL = [
    ('book', 'Livre'),
    ('cd', 'CD'),
    ('dvd', 'DVD'),
    ('parlour_game', 'Jeu de société')
]

CHOICES_MEDIA_LIMITED = [
    ('media', 'Livre / CD / DVD'),
    ('parlour_game', 'Jeu de société')
]

class CreateMedia(forms.Form):
    media_type = forms.ChoiceField(
        required=True,
        choices=CHOICES_MEDIA_FULL,
        label='Type du média',
        widget=forms.Select(attrs={'id': 'media-type-create'})
    )
    name = forms.CharField(required=True, label='Nom')
    author = forms.CharField(required=True, label='Auteur / Artiste / Réalisateur / Créateur')


class DeleteMedia(forms.Form):
    media_type = forms.ChoiceField(
        required=True,
        choices=CHOICES_MEDIA_LIMITED,
        label='Type du média',
        widget=forms.Select(attrs={'id': 'media-type-delete'})
    )
    id = forms.IntegerField(
        required=True,
        label='Identifiant',
        widget=forms.TextInput(attrs={'id': 'media-id-delete'})
    )


class UpdateMedia(forms.Form):
    media_type = forms.ChoiceField(
        required=True,
        choices=CHOICES_MEDIA_LIMITED,
        label='Type du média',
        widget=forms.Select(attrs={'id': 'media-type-update'})
    )
    id = forms.IntegerField(
        required=True,
        label='Identifiant',
        widget=forms.TextInput(attrs={'id': 'media-id-update'})
    )
    name = forms.CharField(
        required=True,
        label='Nom',
        widget=forms.TextInput(attrs={'id': 'media-name-update'})
    )
    author = forms.CharField(
        required=True,
        label='Auteur / Artiste / Réalisateur / Créateur',
        widget=forms.TextInput(attrs={'id': 'media-author-update'})
    )


'''
Members management forms
'''


class CreateMember(forms.Form):
    last_name = forms.CharField(required=True, label='Nom')
    first_name = forms.CharField(required=True, label='Prénom')


class DeleteMember(forms.Form):
    id = forms.IntegerField(
        required=True,
        label='Identifiant',
        widget=forms.TextInput(attrs={'id': 'member-id-delete'})
    )

class UpdateMember(forms.Form):
    id = forms.IntegerField(
        required=True,
        label='Identifiant',
        widget=forms.TextInput(attrs={'id': 'member-id-update'})
    )
    last_name = forms.CharField(
        required=True,
        label='Nom',
        widget=forms.TextInput(attrs={'id': 'member-last-name-update'})
    )
    first_name = forms.CharField(
        required=True,
        label='Prénom',
        widget=forms.TextInput(attrs={'id': 'member-first-name-update'})
    )
    is_blocked = forms.ChoiceField(
        required=True,
        choices=[],
        label="Le membre est interdit d'emprunt",
        widget=forms.Select(attrs={'id': 'member-is-blocked-update'})
    )

'''
Borrowings form
'''


class BorrowingMediaForm(forms.Form):
    media_id = forms.IntegerField(
        required=True,
        label='Identifiant du média',
        initial=0,
        widget=forms.TextInput(attrs={'id': 'media-id-borrow'})
    )
    member_id = forms.IntegerField(
        required=True,
        label='Identifiant du membre',
        initial=0,
        widget=forms.TextInput(attrs={'id': 'member-id-borrow'})
    )


class ReturnMediaForm(forms.Form):
    member_id = forms.IntegerField(
        required=True,
        label='Identifiant du membre',
        initial=0,
        widget=forms.TextInput(attrs={'id': 'member-id-return'})
    )
    media_id = forms.ChoiceField(
        required=True,
        choices = [],
        label='Identifiant du média',
        widget=forms.Select(attrs={'id': 'media-select-return'})
    )