from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from zoneinfo import ZoneInfo
from datetime import timedelta
from librarians_app.models import Book, Member
from librarians_app.forms import CreateBook, DeleteBook, UpdateBook
from librarians_app.forms import CreateMember, UpdateMember, DeleteMember
from librarians_app.forms import BorrowingMediaForm, ReturnMediaForm

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
    #if not book_id:
        #return JsonResponse({'error': 'ID du livre manquant.'})
    try:
        book = Book.objects.get(pk=book_id)
        data = {
            'title': book.name,
            'author': book.author
        }
    except Book.DoesNotExist:
        data = {'error': 'Cet identifiant ne correspond à aucun livre'}
    return JsonResponse(data)

'''
View relative to membersManagement.html
'''

def createMember(request):
    create_member = CreateMember(request.POST)
    if create_member.is_valid():
        member = Member()
        member.first_name = create_member.cleaned_data['first_name']
        member.last_name = create_member.cleaned_data['last_name']
        member.save()
        return redirect('members_management')

def updateMember(request):
    update_member = UpdateMember(request.POST)
    update_member.fields['is_blocked'].choices = [
        ('true', 'Oui'),
        ('false', 'Non')
    ]
    if update_member.is_valid():
        id = update_member.cleaned_data['id']
        member = Member.objects.get(pk=id)
        member.first_name = update_member.cleaned_data['first_name']
        member.last_name = update_member.cleaned_data['last_name']
        is_blocked = update_member.cleaned_data['is_blocked']
        if is_blocked == 'true':
            member.is_blocked = True
        elif is_blocked == 'false':
            member.is_blocked = False
        member.save()
        return redirect('members_management')

def deleteMember(request):
    delete_member = DeleteMember(request.POST)
    if delete_member.is_valid():
        id = delete_member.cleaned_data['id']
        member = Member.objects.get(pk=id)
        member.delete()
        return redirect('members_management')

def membersManagement(request):
    members = Member.objects.all()
    if request.method == 'POST':
        if 'submit_create_member' in request.POST:
            return createMember(request)
        elif 'submit_update_member' in request.POST:
            return updateMember(request)
        elif 'submit_delete_member' in request.POST:
            return deleteMember(request)
    else:
        return render(request, 'membersManagement.html', {
            'members': members,
            'create_member': CreateMember(),
            'update_member': UpdateMember(),
            'delete_member': DeleteMember()
        })

def getMemberDetails(request):
    member_id = request.GET.get("member_id")
    #if not (member_id):
        #return JsonResponse({'error': 'Membre introuvable'})
    try:
        member = Member.objects.get(pk=member_id)
        data = {
            'last_name': member.last_name,
            'first_name': member.first_name,
            'is_blocked': member.is_blocked
        }
    except Member.DoesNotExist:
        data = {'error': 'Cet identifiant ne correspond à aucun membre'}
    return JsonResponse(data)

'''
View relative to borrowings.html
'''

def returnDate(borrowing_date):
    return_day = borrowing_date + timedelta(days=7)
    return_date_time = return_day.replace(hour=23, minute=00)
    return return_date_time

def newBorrowing(request):
    new_borrowing = BorrowingMediaForm(request.POST)
    if new_borrowing.is_valid():
        media_type = new_borrowing.cleaned_data['media_type']
        media_id = new_borrowing.cleaned_data['media_id']
        member_id = new_borrowing.cleaned_data['member_id']
        member = Member.objects.get(pk=member_id)
        if media_type == 'book' :
            book = Book.objects.get(pk=media_id)
            book.borrowing_date = timezone.now().astimezone(ZoneInfo("Europe/Paris"))
            book.return_date = returnDate(timezone.now().astimezone(ZoneInfo("Europe/Paris")))
            book.is_available = False
            book.borrower = member
            member.nb_current_borrowings += 1
            member.save()
            book.save()
    return redirect('borrowings')

def returnMedia(media):
    media.borrowing_date = None
    media.return_date = None
    media.is_available = True
    media.borrower = None
    media.save()

def returnBorrowing(request):
    return_borrowing = ReturnMediaForm(request.POST)
    member_id = request.POST.get('member_id')
    member = Member.objects.get(pk=member_id)
    borrowed_books = Book.objects.filter(borrower=member, is_available=False)
    return_borrowing.fields['media_id'].choices = [
        (book.pk, book.name) for book in borrowed_books
    ]
    if return_borrowing.is_valid():
        member.nb_current_borrowings -= 1
        member.save()
        media_id = return_borrowing.cleaned_data['media_id']
        media_type = request.POST.get('media_type_return')
        if media_type == 'livre':
            media = Book.objects.get(pk=media_id)
            returnMedia(media)
    return redirect('borrowings')

def borrowings(request):
    borrowing_media_form = BorrowingMediaForm()
    books_borrowed = Book.objects.filter(is_available=False)
    if request.method == 'POST':
        if 'submit_borrowing' in request.POST:
            return newBorrowing(request)
        elif 'submit_return' in request.POST:
            return returnBorrowing(request)
    return render(request, 'borrowings.html', {
        'books_borrowed':books_borrowed,
        'borrowing_media_form':borrowing_media_form,
        'return_media_form': ReturnMediaForm()
    })

def getMediaDetails(request):
    media_id = request.GET.get('media_id')
    media_type = request.GET.get('media_type')
    if media_type == "book":
        try:
            book = Book.objects.get(pk=media_id)
            if book.is_available == True:
                data = {
                    'title': book.name,
                    'author': book.author
                }
            else:
                data = {'error': 'Ce livre est déjà emprunté par un membre'}
        except Book.DoesNotExist:
            data = {'error': 'Cet identifiant ne correspond à aucun livre'}
        return JsonResponse(data)
    else:
        data = {'error': "Ce média n'est pas reconnu"}
        return JsonResponse(data)

def getBorrowedMedia(request):
    member_id = request.GET.get('member_id')
    media_data = []

    try:
        member = Member.objects.get(pk=member_id)
        member_data = {'name': f'{member.last_name} {member.first_name}'}
    except Member.DoesNotExist:
        data_error = {'error': 'Cet identifiant ne correspond à aucun membre'}
        return JsonResponse(data_error)

    books = Book.objects.filter(borrower = member)
    for book in books:
        media_data.append({
            'id': book.pk,
            'type': book.media_type,
            'name': book.name,
            'author': book.author
        })
    if media_data == []:
        return JsonResponse({
            'empty': "Aucun emprunt n'est enregistré au nom de ce membre",
            'member_data': member_data
        })
    else:
        return JsonResponse({
            'media_choices': media_data,
            'member_data': member_data
    })


