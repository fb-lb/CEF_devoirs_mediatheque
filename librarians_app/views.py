from django.shortcuts import render, redirect
from django.http import JsonResponse
from librarians_app.models import Book, Member
from librarians_app.forms import CreateBook, DeleteBook, UpdateBook
from librarians_app.forms import CreateMember
from librarians_app.forms import BorrowingMediaForm

'''
View relative to mediaManagement.html
'''

def createBook(request):
    create_book = CreateBook(request.POST)
    if create_book.is_valid():
        book = Book()
        book.name = create_book.cleaned_data['name']
        book.author = create_book.cleaned_data['author']
        book.save()
        return redirect('media_management')

def deleteBook(request):
    delete_book = DeleteBook(request.POST)
    if delete_book.is_valid():
        book = Book.objects.get(pk=delete_book.cleaned_data['id'])
        book.delete()
        return redirect('media_management')

def updateBook(request):
    update_book = UpdateBook(request.POST)
    if update_book.is_valid():
        id = update_book.cleaned_data['id']
        book = Book.objects.get(pk=id)
        book.name = update_book.cleaned_data['name']
        book.author = update_book.cleaned_data['author']
        book.save()
        return redirect('media_management')

def mediaManagement(request):
    if request.method == 'POST':
        if 'submit_create_book' in request.POST:
            return createBook(request)
        elif 'submit_delete_book' in request.POST:
            return deleteBook(request)
        elif 'submit_update_book' in request.POST:
            return updateBook(request)
    else:
        return render(request, 'mediaManagement.html', {
            'create_book': CreateBook(),
            'delete_book': DeleteBook(),
            'update_book': UpdateBook()
        })

def getBookDetails(request):
    book_id = request.GET.get('book_id')
    if not book_id:
        return JsonResponse({'error': 'ID du livre manquant.'})
    try:
        book = Book.objects.get(pk=book_id)
        data = {
            'title': book.name,
            'author': book.author
        }
    except Book.DoesNotExist:
        data = {'error': 'Livre non trouvé'}
    return JsonResponse(data)

'''
View relative to membersManagement.html
'''

def createMember(request, members):
    create_member = CreateMember(request.POST)
    if create_member.is_valid():
        member = Member()
        member.first_name = create_member.cleaned_data['first_name']
        member.last_name = create_member.cleaned_data['last_name']
        member.save()
        return redirect('members_management')

def membersManagement(request):
    members = Member.objects.all()
    if request.method == 'POST':
        if 'submit_create_member' in request.POST:
            return createMember(request, members)
    else:
        return render(request, 'membersManagement.html', {
            'members': members,
            'create_member': CreateMember()
        })

'''
View relative to borrowings.html
'''

def borrowings(request):
    books_borrowed = Book.objects.filter(is_available=False)
    borrowing_media_form = BorrowingMediaForm
    return render(request, 'borrowings.html', {'books_borrowed':books_borrowed, 'borrowing_media_form':borrowing_media_form})