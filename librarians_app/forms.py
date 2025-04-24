from django import forms

'''
Books management forms
'''


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

'''
Borrowings form
'''

CHOICES_BORROWING = [
    ('book', 'Livre'),
    ('cd', 'CD')
]


class BorrowingMediaForm(forms.Form):
    media_type = forms.ChoiceField(
        choices=CHOICES_BORROWING,
        initial='Livre',
        label='Type du média',
        widget=forms.Select(attrs={'id': 'media-type-borrow'})
    )
    media_id = forms.IntegerField(
        label='Identifiant du média',
        initial=0,
        widget=forms.TextInput(attrs={'id': 'media-id-borrow'})
    )
    member_id = forms.IntegerField(
        label='Identifiant du membre',
        initial=0,
        widget=forms.TextInput(attrs={'id': 'member-id-borrow'})
    )


class ReturnMediaForm(forms.Form):
    member_id = forms.IntegerField(
        label='Identifiant du membre',
        initial=0,
        widget=forms.TextInput(attrs={'id': 'member-id-return'})
    )
    media_id = forms.ChoiceField(
        choices = [],
        label='Identifiant du média',
        widget=forms.Select(attrs={'id': 'media-select-return'})
    )
    '''
    media_id = forms.IntegerField(
        label='Identifiant du média',
        initial=0,
        widget=forms.TextInput(attrs={'id': 'media-id-return'})
    )
    '''