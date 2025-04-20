from django import forms


class CreateBook(forms.Form):
    name = forms.CharField(required=True, label='Nom')
    author = forms.CharField(required=True, label='Auteur')


class DeleteBook(forms.Form):
    id = forms.IntegerField(
        required=True,
        label='Identifiant',
        widget=forms.TextInput(attrs={'id': 'book-id-delete'})
    )


class UpdateBook(forms.Form):
    id = forms.IntegerField(
        required=True,
        label='Identifiant',
        widget=forms.TextInput(attrs={'id': 'book-id-update'})
    )
    name = forms.CharField(
        required=True,
        label='Nom',
        widget=forms.TextInput(attrs={'id': 'book-name-update'})
    )
    author = forms.CharField(
        required=True,
        label='Auteur',
        widget=forms.TextInput(attrs={'id': 'book-author-update'})
    )


CHOICES = [
    ('option2', 'Livre'),
    ('option3', 'CD')
]


class BorrowingMediaForm(forms.Form):
    media_type = forms.ChoiceField(choices=CHOICES, initial='option1', label='Type du média')
    id = forms.IntegerField(label='Identifiant', initial=0)
