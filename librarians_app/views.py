from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.utils import timezone
from zoneinfo import ZoneInfo
from datetime import timedelta, date
from librarians_app.models import Book, Cd, Dvd, ParlourGame, Member
from librarians_app.forms import CreateMedia, DeleteMedia, UpdateMedia
from librarians_app.forms import CreateMember, UpdateMember, DeleteMember
from librarians_app.forms import BorrowingMediaForm, ReturnMediaForm

'''
View relative to mediaManagement.html
'''

def createMedia(request):
    create_media = CreateMedia(request.POST)
    if create_media.is_valid():
        media_type = create_media.cleaned_data['media_type']
        if media_type == 'book':
            book = Book()
            book.name = create_media.cleaned_data['name']
            book.author = create_media.cleaned_data['author']
            book.save()
            return redirect(reverse('media_management') + '?success=create_media#create-media-section')
        elif media_type == 'cd':
            cd = Cd()
            cd.name = create_media.cleaned_data['name']
            cd.artist = create_media.cleaned_data['author']
            cd.save()
            return redirect(reverse('media_management') + '?success=create_media#create-media-section')
        elif media_type == 'dvd':
            dvd = Dvd()
            dvd.name = create_media.cleaned_data['name']
            dvd.director = create_media.cleaned_data['author']
            dvd.save()
            return redirect(reverse('media_management') + '?success=create_media#create-media-section')
        elif media_type == 'parlour_game':
            parlour_game = ParlourGame()
            parlour_game.name = create_media.cleaned_data['name']
            parlour_game.creator = create_media.cleaned_data['author']
            parlour_game.save()
            return redirect(reverse('media_management') + '?success=create_media#create-media-section')
        else:
            return redirect(reverse('media_management') + '?error_media_type=create_media#create-media-section')
    else:
        return render(request, 'mediaManagement.html', {
            'create_media': create_media,
            'delete_media': DeleteMedia(),
            'update_media': UpdateMedia(),
            'anchor': 'create-media-section'
        })

def deleteMedia(request):
    delete_media = DeleteMedia(request.POST)
    if delete_media.is_valid():
        media_type = delete_media.cleaned_data['media_type']
        if media_type == 'book':
            try :
                book = Book.objects.get(pk=delete_media.cleaned_data['id'])
                book.delete()
                return redirect(reverse('media_management') + '?success=delete_media#delete-media-section')
            except Book.DoesNotExist:
                return redirect(reverse('media_management') + '?error=delete_book#delete-media-section')
        elif media_type == 'cd':
            try :
                cd = Cd.objects.get(pk=delete_media.cleaned_data['id'])
                cd.delete()
                return redirect(reverse('media_management') + '?success=delete_media#delete-media-section')
            except Cd.DoesNotExist:
                return redirect(reverse('media_management') + '?error=delete_cd#delete-media-section')
        elif media_type == 'dvd':
            try :
                dvd = Dvd.objects.get(pk=delete_media.cleaned_data['id'])
                dvd.delete()
                return redirect(reverse('media_management') + '?success=delete_media#delete-media-section')
            except Dvd.DoesNotExist:
                return redirect(reverse('media_management') + '?error=delete_dvd#delete-media-section')
        elif media_type == 'parlour_game':
            try :
                parlour_game = ParlourGame.objects.get(pk=delete_media.cleaned_data['id'])
                parlour_game.delete()
                return redirect(reverse('media_management') + '?success=delete_media#delete-media-section')
            except ParlourGame.DoesNotExist:
                return redirect(reverse('media_management') + '?error=delete_parlour_game#delete-media-section')
        else:
            return redirect(reverse('media_management') + '?error=delete_media_type#delete-media-section')
    else:
        return render(request, 'mediaManagement.html', {
            'create_media': CreateMedia(),
            'delete_media': delete_media,
            'update_media': UpdateMedia(),
            'anchor': 'delete-media-section'
        })

def updateMedia(request):
    update_media = UpdateMedia(request.POST)
    if update_media.is_valid():
        media_type = update_media.cleaned_data['media_type']
        if media_type == 'book':
            try:
                id = update_media.cleaned_data['id']
                book = Book.objects.get(pk=id)
                book.name = update_media.cleaned_data['name']
                book.author = update_media.cleaned_data['author']
                book.save()
                return redirect(reverse('media_management') + '?success=update_media#update-media-section')
            except Book.DoesNotExist:
                return redirect(reverse('media_management') + '?error=update_book#update-media-section')
        elif media_type == 'cd':
            try:
                id = update_media.cleaned_data['id']
                cd = Cd.objects.get(pk=id)
                cd.name = update_media.cleaned_data['name']
                cd.artist = update_media.cleaned_data['author']
                cd.save()
                return redirect(reverse('media_management') + '?success=update_media#update-media-section')
            except Cd.DoesNotExist:
                return redirect(reverse('media_management') + '?error=update_cd#update-media-section')
        elif media_type == 'dvd':
            try:
                id = update_media.cleaned_data['id']
                dvd = Dvd.objects.get(pk=id)
                dvd.name = update_media.cleaned_data['name']
                dvd.director = update_media.cleaned_data['author']
                dvd.save()
                return redirect(reverse('media_management') + '?success=update_media#update-media-section')
            except Dvd.DoesNotExist:
                return redirect(reverse('media_management') + '?error=update_dvd#update-media-section')
        elif media_type == 'parlour_game':
            try:
                id = update_media.cleaned_data['id']
                parlour_game = ParlourGame.objects.get(pk=id)
                parlour_game.name = update_media.cleaned_data['name']
                parlour_game.creator = update_media.cleaned_data['author']
                parlour_game.save()
                return redirect(reverse('media_management') + '?success=update_media#update-media-section')
            except ParlourGame.DoesNotExist:
                return redirect(reverse('media_management') + '?error=update_parlour_game#update-media-section')
        else:
            return redirect(reverse('media_management') + '?error=update_media_type#update-media-section')
    else:
        return render(request, 'mediaManagement.html', {
            'create_media': CreateMedia(),
            'delete_media': DeleteMedia(),
            'update_media': update_media,
            'anchor': 'update-media-section'
        })

def mediaManagement(request):
    if request.method == 'POST':
        if 'submit_create_media' in request.POST:
            return createMedia(request)
        elif 'submit_delete_media' in request.POST:
            return deleteMedia(request)
        elif 'submit_update_media' in request.POST:
            return updateMedia(request)
        else:
            return redirect('media_management')
    else:
        return render(request, 'mediaManagement.html', {
            'create_media': CreateMedia(),
            'delete_media': DeleteMedia(),
            'update_media': UpdateMedia()
        })

def getMediaDetailsManagement(request):
    media_id = request.GET.get('media_id')
    media_type = request.GET.get('media_type')
    if media_type == 'book':
        try:
            book = Book.objects.get(pk=media_id)
            data = {
                'title': book.name,
                'author': book.author
            }
            return JsonResponse(data)
        except Book.DoesNotExist:
            data = {'error': 'Cet identifiant ne correspond à aucun livre'}
            return JsonResponse(data)
    elif media_type == 'cd':
        try:
            cd = Cd.objects.get(pk=media_id)
            data = {
                'title': cd.name,
                'author': cd.artist
            }
            return JsonResponse(data)
        except Cd.DoesNotExist:
            data = {'error': 'Cet identifiant ne correspond à aucun CD'}
            return JsonResponse(data)
    elif media_type == 'dvd':
        try:
            dvd = Dvd.objects.get(pk=media_id)
            data = {
                'title': dvd.name,
                'author': dvd.director
            }
            return JsonResponse(data)
        except Dvd.DoesNotExist:
            data = {'error': 'Cet identifiant ne correspond à aucun DVD'}
            return JsonResponse(data)
    elif media_type == 'parlour_game':
        try:
            parlour_game = ParlourGame.objects.get(pk=media_id)
            data = {
                'title': parlour_game.name,
                'author': parlour_game.creator
            }
            return JsonResponse(data)
        except ParlourGame.DoesNotExist:
            data = {'error': 'Cet identifiant ne correspond à aucun jeu de société'}
            return JsonResponse(data)
    else:
        data = {'error': "Ce type de média n'existe pas dans notre base de données"}
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
        return redirect(reverse('members_management') + '?success=create_member#create-member-section')
    else:
        return render(request, 'membersManagement.html', {
            'members': members,
            'create_member': create_member,
            'update_member': UpdateMember(),
            'delete_member': DeleteMember(),
            'anchor': 'create-member-section'
        })

def updateMember(request, members):
    update_member = UpdateMember(request.POST)
    update_member.fields['is_blocked'].choices = [
        ('true', 'Oui'),
        ('false', 'Non')
    ]
    if update_member.is_valid():
        try:
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
            return redirect(reverse('members_management') + '?success=update_member#update-member-section')
        except Member.DoesNotExist:
            return redirect(reverse('members_management') + '?error=update_member#update-member-section')
    else:
        return render(request, 'membersManagement.html', {
            'members': members,
            'create_member': CreateMember(),
            'update_member': update_member,
            'delete_member': DeleteMember(),
            'anchor': 'update-member-section'
        })

def deleteMember(request, members):
    delete_member = DeleteMember(request.POST)
    if delete_member.is_valid():
        try:
            id = delete_member.cleaned_data['id']
            member = Member.objects.get(pk=id)
            if member.nb_current_borrowings > 0:
                return redirect(reverse('members_management') + '?no_delete=delete_member#delete-member-section')
            else:
                member.delete()
                return redirect(reverse('members_management') + '?success=delete_member#delete-member-section')
        except Member.DoesNotExist:
            return redirect(reverse('members_management') + '?error=delete_member#delete-member-section')
    else:
        return render(request, 'memberManagement.html', {
            'members': members,
            'create_member': CreateMember(),
            'update_member': UpdateMember(),
            'delete_member': delete_member,
            'anchor': 'delete-member-section'
        })

def membersManagement(request):
    members = Member.objects.all()
    if request.method == 'POST':
        if 'submit_create_member' in request.POST:
            return createMember(request, members)
        elif 'submit_update_member' in request.POST:
            return updateMember(request, members)
        elif 'submit_delete_member' in request.POST:
            return deleteMember(request, members)
    else:
        return render(request, 'membersManagement.html', {
            'members': members,
            'create_member': CreateMember(),
            'update_member': UpdateMember(),
            'delete_member': DeleteMember()
        })

def getMemberDetails(request):
    member_id = request.GET.get("member_id")
    try:
        member = Member.objects.get(pk=member_id)
        data = {
            'last_name': member.last_name,
            'first_name': member.first_name,
            'is_blocked': member.is_blocked,
            'nb_current_borrowings' : member.nb_current_borrowings
        }
    except Member.DoesNotExist:
        data = {'error': 'Cet identifiant ne correspond à aucun membre'}
    return JsonResponse(data)

'''
View relative to borrowings.html
'''

def isMemberBlocked(member):
    is_blocked = False
    today = date.today()
    borrowed_books = Book.objects.filter(borrower=member, is_available=False)
    for book in borrowed_books:
        if book.return_date < today:
            is_blocked = True
    member.is_blocked = is_blocked
    member.save()

def returnDate(borrowing_date):
    return_day = borrowing_date + timedelta(days=7)
    return_date_time = return_day.replace(hour=23, minute=00)
    return return_date_time

def newBorrowing(request, books_borrowed, cd_borrowed, dvd_borrowed):
    new_borrowing = BorrowingMediaForm(request.POST)
    if new_borrowing.is_valid():
        media_type = new_borrowing.cleaned_data['media_type']
        media_id = new_borrowing.cleaned_data['media_id']
        member_id = new_borrowing.cleaned_data['member_id']
        try:
            member = Member.objects.get(pk=member_id)
        except Member.DoesNotExist:
            return redirect(reverse('borrowings') + '?error_member=borrowing_media#borrowing-media-section')
        isMemberBlocked(member)
        member = Member.objects.get(pk=member_id)
        if member.is_blocked == True:
            return redirect(reverse('borrowings') + '?error_blocked=borrowing_media#borrowing-media-section')
        if member.nb_current_borrowings >= 3:
            return redirect(reverse('borrowings') + '?error_too_much_borrowings=borrowing_media#borrowing-media-section')
        if media_type == 'book' :
            try:
                book = Book.objects.get(pk=media_id)
                if book.is_available==False:
                    return redirect(reverse('borrowings') + '?error_not_available=borrowing_media#borrowing-media-section')
                book.borrowing_date = timezone.now().astimezone(ZoneInfo("Europe/Paris"))
                book.return_date = returnDate(timezone.now().astimezone(ZoneInfo("Europe/Paris")))
                book.is_available = False
                book.borrower = member
                member.nb_current_borrowings += 1
                member.save()
                book.save()
                return redirect(reverse('borrowings') + '?success=borrowing_media#borrowing-media-section')
            except Book.DoesNotExist:
                return redirect(reverse('borrowings') + '?error_book=borrowing_media#borrowing-media-section')
        elif media_type == 'cd' :
            try:
                cd = Cd.objects.get(pk=media_id)
                if cd.is_available==False:
                    return redirect(reverse('borrowings') + '?error_not_available=borrowing_media#borrowing-media-section')
                cd.borrowing_date = timezone.now().astimezone(ZoneInfo("Europe/Paris"))
                cd.return_date = returnDate(timezone.now().astimezone(ZoneInfo("Europe/Paris")))
                cd.is_available = False
                cd.borrower = member
                member.nb_current_borrowings += 1
                member.save()
                cd.save()
                return redirect(reverse('borrowings') + '?success=borrowing_media#borrowing-media-section')
            except Cd.DoesNotExist:
                return redirect(reverse('borrowings') + '?error_cd=borrowing_media#borrowing-media-section')
        elif media_type == 'dvd' :
            try:
                dvd = Dvd.objects.get(pk=media_id)
                if dvd.is_available==False:
                    return redirect(reverse('borrowings') + '?error_not_available=borrowing_media#borrowing-media-section')
                dvd.borrowing_date = timezone.now().astimezone(ZoneInfo("Europe/Paris"))
                dvd.return_date = returnDate(timezone.now().astimezone(ZoneInfo("Europe/Paris")))
                dvd.is_available = False
                dvd.borrower = member
                member.nb_current_borrowings += 1
                member.save()
                dvd.save()
                return redirect(reverse('borrowings') + '?success=borrowing_media#borrowing-media-section')
            except Dvd.DoesNotExist:
                return redirect(reverse('borrowings') + '?error_dvd=borrowing_media#borrowing-media-section')
        else:
            return redirect(reverse('borrowings') + '?error_media_type=borrowing_media#borrowing-media-section')
    else:
        return render(request, 'borrowings.html', {
            'books_borrowed': books_borrowed,
            'cd_borrowed': cd_borrowed,
            'dvd_borrowed': dvd_borrowed,
            'borrowing_media_form': new_borrowing,
            'return_media_form': ReturnMediaForm(),
            'anchor' : 'borrowing-media-section'
        })

def returnedMedia(media):
    media.borrowing_date = None
    media.return_date = None
    media.is_available = True
    media.borrower = None
    media.save()

def returnBorrowing(request, books_borrowed, cd_borrowed, dvd_borrowed):
    return_borrowing = ReturnMediaForm(request.POST)
    member_id = request.POST.get('member_id')
    if not member_id:
        return render(request, 'borrowings.html', {
            'books_borrowed': books_borrowed,
            'cd_borrowed': cd_borrowed,
            'dvd_borrowed': dvd_borrowed,
            'borrowing_media_form': BorrowingMediaForm(),
            'return_media_form': return_borrowing,
            'anchor': 'return-media-section'
        })
    try:
        member = Member.objects.get(pk=member_id)
    except Member.DoesNotExist:
        return redirect(reverse('borrowings') + '?error_member=return_media#return-media-section')
    borrowed_books = Book.objects.filter(borrower=member, is_available=False)
    borrowed_cds = Cd.objects.filter(borrower=member, is_available=False)
    borrowed_dvds = Dvd.objects.filter(borrower=member, is_available=False)
    return_borrowing.fields['media_id'].choices = [
        *[(book.pk, book.name) for book in borrowed_books],
        *[(cd.pk, cd.name) for cd in borrowed_cds],
        *[(dvd.pk, dvd.name) for dvd in borrowed_dvds]
    ]
    if return_borrowing.is_valid():
        member.nb_current_borrowings -= 1
        media_id = return_borrowing.cleaned_data['media_id']
        media_type = request.POST.get('media_type_return')
        if media_type == 'livre':
            try:
                media = Book.objects.get(pk=media_id)
                returnedMedia(media)
                member.save()
                isMemberBlocked(member)
                return redirect(reverse('borrowings') + '?success=return_media#return-media-section')
            except Book.DoesNotExist:
                return redirect(reverse('borrowings') + '?error_book=return_media#return-media-section')
        elif media_type == 'cd':
            try:
                media = Cd.objects.get(pk=media_id)
                returnedMedia(media)
                member.save()
                isMemberBlocked(member)
                return redirect(reverse('borrowings') + '?success=return_media#return-media-section')
            except Cd.DoesNotExist:
                return redirect(reverse('borrowings') + '?error_cd=return_media#return-media-section')
        elif media_type == 'dvd':
            try:
                media = Dvd.objects.get(pk=media_id)
                returnedMedia(media)
                member.save()
                isMemberBlocked(member)
                return redirect(reverse('borrowings') + '?success=return_media#return-media-section')
            except Dvd.DoesNotExist:
                return redirect(reverse('borrowings') + '?error_dvd=return_media#return-media-section')
        else:
            return redirect(reverse('borrowings') + '?error_media_type=return_media#return-media-section')
    else:
        return render(request, 'borrowings.html', {
            'books_borrowed':books_borrowed,
            'cd_borrowed': cd_borrowed,
            'dvd_borrowed': dvd_borrowed,
            'borrowing_media_form':BorrowingMediaForm(),
            'return_media_form': return_borrowing,
            'anchor': 'return-media-section'
    })

def borrowings(request):
    books_borrowed = Book.objects.filter(is_available=False)
    cd_borrowed = Cd.objects.filter(is_available=False)
    dvd_borrowed = Dvd.objects.filter(is_available=False)
    if request.method == 'POST':
        if 'submit_borrowing' in request.POST:
            return newBorrowing(request, books_borrowed, cd_borrowed, dvd_borrowed)
        elif 'submit_return' in request.POST:
            return returnBorrowing(request, books_borrowed, cd_borrowed, dvd_borrowed)
    return render(request, 'borrowings.html', {
        'books_borrowed': books_borrowed,
        'cd_borrowed': cd_borrowed,
        'dvd_borrowed': dvd_borrowed,
        'borrowing_media_form': BorrowingMediaForm(),
        'return_media_form': ReturnMediaForm()
    })

def getMediaDetailsBorrowing(request):
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
    elif media_type == "cd":
        try:
            cd = Cd.objects.get(pk=media_id)
            if cd.is_available == True:
                data = {
                    'title': cd.name,
                    'author': cd.artist
                }
            else:
                data = {'error': 'Ce CD est déjà emprunté par un membre'}
        except Cd.DoesNotExist:
            data = {'error': 'Cet identifiant ne correspond à aucun CD'}
        return JsonResponse(data)
    elif media_type == "dvd":
        try:
            dvd = Dvd.objects.get(pk=media_id)
            if dvd.is_available == True:
                data = {
                    'title': dvd.name,
                    'author': dvd.director
                }
            else:
                data = {'error': 'Ce DVD est déjà emprunté par un membre'}
        except Dvd.DoesNotExist:
            data = {'error': 'Cet identifiant ne correspond à aucun DVD'}
        return JsonResponse(data)
    else:
        data = {'error': "Ce média n'est pas reconnu"}
        return JsonResponse(data)

def getBorrowedMedia(request):
    member_id = request.GET.get('member_id')
    media_choices = []

    try:
        member = Member.objects.get(pk=member_id)
        member_data = {'name': f'{member.last_name} {member.first_name}'}
    except Member.DoesNotExist:
        data_error = {'error': 'Cet identifiant ne correspond à aucun membre'}
        return JsonResponse(data_error)

    books = Book.objects.filter(borrower=member)
    for book in books:
        media_choices.append({
            'id': book.pk,
            'type': book.media_type,
            'name': book.name,
            'author': book.author,
            'borrowing_date': book.borrowing_date,
            'return_date': book.return_date
        })
    cds = Cd.objects.filter(borrower=member)
    for cd in cds:
        media_choices.append({
            'id': cd.pk,
            'type': cd.media_type,
            'name': cd.name,
            'author': cd.artist,
            'borrowing_date': cd.borrowing_date,
            'return_date': cd.return_date
        })
    dvds = Dvd.objects.filter(borrower=member)
    for dvd in dvds:
        media_choices.append({
            'id': dvd.pk,
            'type': dvd.media_type,
            'name': dvd.name,
            'author': dvd.director,
            'borrowing_date': dvd.borrowing_date,
            'return_date': dvd.return_date
        })
    if not media_choices:
        return JsonResponse({
            'empty': "Aucun emprunt n'est enregistré au nom de ce membre",
            'member_data': member_data
        })
    else:
        return JsonResponse({
            'media_choices': media_choices,
            'member_data': member_data
    })