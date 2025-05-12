from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from datetime import timedelta, date
from librarians_app.models import BorrowableMedia, Book, Cd, Dvd, ParlourGame, Member
from librarians_app.forms import CreateMedia, DeleteMedia, UpdateMedia
from librarians_app.forms import CreateMember, UpdateMember, DeleteMember
from librarians_app.forms import BorrowingMediaForm, ReturnMediaForm

'''
View relative to mediaManagement.html
'''

def create_media(request, medias, parlour_games):
    create_media_request = CreateMedia(request.POST)
    if create_media_request.is_valid():
        media_type = create_media_request.cleaned_data['media_type']
        if media_type == 'book':
            book = Book()
            book.name = create_media_request.cleaned_data['name']
            book.author = create_media_request.cleaned_data['author']
            book.save()
            return redirect(reverse('media_management') + '?success=create_media#create-media-section')
        elif media_type == 'cd':
            cd = Cd()
            cd.name = create_media_request.cleaned_data['name']
            cd.artist = create_media_request.cleaned_data['author']
            cd.save()
            return redirect(reverse('media_management') + '?success=create_media#create-media-section')
        elif media_type == 'dvd':
            dvd = Dvd()
            dvd.name = create_media_request.cleaned_data['name']
            dvd.director = create_media_request.cleaned_data['author']
            dvd.save()
            return redirect(reverse('media_management') + '?success=create_media#create-media-section')
        elif media_type == 'parlour_game':
            parlour_game = ParlourGame()
            parlour_game.name = create_media_request.cleaned_data['name']
            parlour_game.creator = create_media_request.cleaned_data['author']
            parlour_game.save()
            return redirect(reverse('media_management') + '?success=create_media#create-media-section')
        else:
            return redirect(reverse('media_management') + '?error_media_type=create_media#create-media-section')
    else:
        return render(request, 'mediaManagement.html', {
            'create_media': create_media_request,
            'delete_media': DeleteMedia(),
            'update_media': UpdateMedia(),
            'medias': medias,
            'parlour_games': parlour_games,
            'anchor': 'create-media-section'
        })

def delete_media(request, medias, parlour_games):
    delete_media_request = DeleteMedia(request.POST)
    if delete_media_request.is_valid():
        media_type = delete_media_request.cleaned_data['media_type']
        if media_type == 'media':
            try:
                media = BorrowableMedia.objects.get(pk=delete_media_request.cleaned_data['id'])
                media.delete()
                return redirect(reverse('media_management') + '?success=delete_media#delete-media-section')
            except BorrowableMedia.DoesNotExist:
                return redirect(reverse('media_management') + '?error=delete_media#delete-media-section')
        elif media_type == 'parlour_game':
            try :
                parlour_game = ParlourGame.objects.get(pk=delete_media_request.cleaned_data['id'])
                parlour_game.delete()
                return redirect(reverse('media_management') + '?success=delete_media#delete-media-section')
            except ParlourGame.DoesNotExist:
                return redirect(reverse('media_management') + '?error=delete_parlour_game#delete-media-section')
        else:
            return redirect(reverse('media_management') + '?error=delete_media_type#delete-media-section')
    else:
        return render(request, 'mediaManagement.html', {
            'create_media': CreateMedia(),
            'delete_media': delete_media_request,
            'update_media': UpdateMedia(),
            'medias': medias,
            'parlour_games': parlour_games,
            'anchor': 'delete-media-section'
        })

def update_media(request, medias, parlour_games):
    update_media_request = UpdateMedia(request.POST)
    if update_media_request.is_valid():
        media_type = update_media_request.cleaned_data['media_type']
        if media_type == 'media':
            try:
                id = update_media_request.cleaned_data['id']
                media = BorrowableMedia.objects.get(pk=id)
                media.name = update_media_request.cleaned_data['name']
                if hasattr(media, 'book'):
                    media.book.author = update_media_request.cleaned_data['author']
                    media.book.save()
                elif hasattr(media, 'cd'):
                    media.cd.artist = update_media_request.cleaned_data['author']
                    media.cd.save()
                elif hasattr(media, 'dvd'):
                    media.dvd.director = update_media_request.cleaned_data['author']
                    media.dvd.save()
                else:
                    return redirect(reverse('media_management') + '?error=update_media#update-media-section')
                media.save()
                return redirect(reverse('media_management') + '?success=update_media#update-media-section')
            except BorrowableMedia.DoesNotExist:
                return redirect(reverse('media_management') + '?error=update_media#update-media-section')
        elif media_type == 'parlour_game':
            try:
                id = update_media_request.cleaned_data['id']
                parlour_game = ParlourGame.objects.get(pk=id)
                parlour_game.name = update_media_request.cleaned_data['name']
                parlour_game.creator = update_media_request.cleaned_data['author']
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
            'update_media': update_media_request,
            'medias': medias,
            'parlour_games': parlour_games,
            'anchor': 'update-media-section'
        })

@login_required
def media_management(request):
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
    if request.method == 'POST':
        if 'submit_create_media' in request.POST:
            return create_media(request, medias, parlour_games)
        elif 'submit_delete_media' in request.POST:
            return delete_media(request, medias, parlour_games)
        elif 'submit_update_media' in request.POST:
            return update_media(request, medias, parlour_games)
        else:
            return redirect('media_management')
    else:
        return render(request, 'mediaManagement.html', {
            'create_media': CreateMedia(),
            'delete_media': DeleteMedia(),
            'update_media': UpdateMedia(),
            'medias': medias,
            'parlour_games': parlour_games
        })

def get_media_details_management(request):
    media_id = request.GET.get('media_id')
    media_type = request.GET.get('media_type')

    if media_type == 'media':
        try:
            media = BorrowableMedia.objects.get(pk=media_id)
            data = {'title': media.name}
            if hasattr(media, 'book'):
                data['author'] = media.book.author
            elif hasattr(media, 'cd'):
                data['author'] = media.cd.artist
            elif hasattr(media, 'dvd'):
                data['author'] = media.dvd.director
            else:
                data = {'error': "Ce type de média n'est pas reconnu"}
            return JsonResponse(data)
        except BorrowableMedia.DoesNotExist:
            data = {'error': 'Cet identifiant ne correspond à aucun livre, CD ou DVD'}
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

def create_member(request, members):
    create_member_request = CreateMember(request.POST)
    if create_member_request.is_valid():
        member = Member()
        member.first_name = create_member_request.cleaned_data['first_name']
        member.last_name = create_member_request.cleaned_data['last_name']
        member.save()
        return redirect(reverse('members_management') + '?success=create_member#create-member-section')
    else:
        return render(request, 'membersManagement.html', {
            'members': members,
            'create_member': create_member_request,
            'update_member': UpdateMember(),
            'delete_member': DeleteMember(),
            'anchor': 'create-member-section'
        })

def update_member(request, members):
    update_member_request = UpdateMember(request.POST)
    update_member_request.fields['is_blocked'].choices = [
        ('true', 'Oui'),
        ('false', 'Non')
    ]
    if update_member_request.is_valid():
        try:
            id = update_member_request.cleaned_data['id']
            member = Member.objects.get(pk=id)
            member.first_name = update_member_request.cleaned_data['first_name']
            member.last_name = update_member_request.cleaned_data['last_name']
            is_blocked = update_member_request.cleaned_data['is_blocked']
            if is_blocked == 'true':
                member.is_blocked = True
            elif is_blocked == 'false':
                member.is_blocked = False
                medias = BorrowableMedia.objects.filter(is_available=False, borrower=member)
                today = date.today()
                for media in medias:
                    if media.return_date < today:
                        media.borrower.is_blocked = True
                        media.borrower.save()
                        return redirect(reverse('members_management') + '?error_blocked=update_member#update-member-section')
            member.save()
            return redirect(reverse('members_management') + '?success=update_member#update-member-section')
        except Member.DoesNotExist:
            return redirect(reverse('members_management') + '?error=update_member#update-member-section')
    else:
        return render(request, 'membersManagement.html', {
            'members': members,
            'create_member': CreateMember(),
            'update_member': update_member_request,
            'delete_member': DeleteMember(),
            'anchor': 'update-member-section'
        })

def delete_member(request, members):
    delete_member_request = DeleteMember(request.POST)
    if delete_member_request.is_valid():
        try:
            id = delete_member_request.cleaned_data['id']
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
            'delete_member': delete_member_request,
            'anchor': 'delete-member-section'
        })

@login_required
def members_management(request):
    members = Member.objects.all()
    if request.method == 'POST':
        if 'submit_create_member' in request.POST:
            return create_member(request, members)
        elif 'submit_update_member' in request.POST:
            return update_member(request, members)
        elif 'submit_delete_member' in request.POST:
            return delete_member(request, members)
        else:
            return redirect('members_management')
    else:
        medias = BorrowableMedia.objects.filter(is_available=False)
        today = date.today()
        for media in medias:
            if media.return_date < today:
                media.borrower.is_blocked = True
                media.borrower.save()
        return render(request, 'membersManagement.html', {
            'members': members,
            'create_member': CreateMember(),
            'update_member': UpdateMember(),
            'delete_member': DeleteMember()
        })

def get_member_details(request):
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

def is_member_blocked(member):
    is_blocked = False
    today = date.today()
    borrowed_medias = BorrowableMedia.objects.filter(borrower=member, is_available=False)
    for media in borrowed_medias:
        if media.return_date < today:
            is_blocked = True
    member.is_blocked = is_blocked
    member.save()

def new_borrowing(request, medias_borrowed):
    new_borrowing_request = BorrowingMediaForm(request.POST)
    if new_borrowing_request.is_valid():
        media_id = new_borrowing_request.cleaned_data['media_id']
        member_id = new_borrowing_request.cleaned_data['member_id']
        try:
            member = Member.objects.get(pk=member_id)
        except Member.DoesNotExist:
            return redirect(reverse('borrowings') + '?error_member=borrowing_media#borrowing-media-section')
        is_member_blocked(member)
        member = Member.objects.get(pk=member_id)
        if member.is_blocked == True:
            return redirect(reverse('borrowings') + '?error_blocked=borrowing_media#borrowing-media-section')
        if member.nb_current_borrowings >= 3:
            return redirect(reverse('borrowings') + '?error_too_much_borrowings=borrowing_media#borrowing-media-section')
        try:
            media = BorrowableMedia.objects.get(pk=media_id)
            if media.is_available == False:
                return redirect(reverse('borrowings') + '?error_not_available=borrowing_media#borrowing-media-section')
            else:
                media.borrowing_date = date.today()
                media.return_date =  media.borrowing_date + timedelta(days=7)
                media.is_available = False
                media.borrower = member
                member.nb_current_borrowings += 1
                member.save()
                media.save()
                return redirect(reverse('borrowings') + '?success=borrowing_media#borrowing-media-section')
        except BorrowableMedia.DoesNotExist:
            return redirect(reverse('borrowings') + '?error_media=borrowing_media#borrowing-media-section')
    else:
        return render(request, 'borrowings.html', {
            'medias_borrowed': medias_borrowed,
            'borrowing_media_form': new_borrowing_request,
            'return_media_form': ReturnMediaForm(),
            'anchor' : 'borrowing-media-section'
        })

def return_borrowing(request, medias_borrowed):
    return_borrowing_request = ReturnMediaForm(request.POST)
    member_id = request.POST.get('member_id')
    if not member_id:
        return render(request, 'borrowings.html', {
            'medias_borrowed': medias_borrowed,
            'borrowing_media_form': BorrowingMediaForm(),
            'return_media_form': return_borrowing_request,
            'anchor': 'return-media-section'
        })
    try:
        member = Member.objects.get(pk=member_id)
    except Member.DoesNotExist:
        return redirect(reverse('borrowings') + '?error_member=return_media#return-media-section')
    borrowed_medias = BorrowableMedia.objects.filter(borrower=member, is_available=False)
    return_borrowing_request.fields['media_id'].choices = [(media.pk, media.name) for media in borrowed_medias]
    if return_borrowing_request.is_valid():
        media_id = return_borrowing_request.cleaned_data['media_id']
        try:
            media = BorrowableMedia.objects.get(pk=media_id)
            media.borrowing_date = None
            media.return_date = None
            media.is_available = True
            media.borrower = None
            member.nb_current_borrowings -= 1
            media.save()
            member.save()
            is_member_blocked(member)
            return redirect(reverse('borrowings') + '?success=return_media#return-media-section')
        except BorrowableMedia.DoesNotExist:
            return redirect(reverse('borrowings') + '?error_media=return_media#return-media-section')
    else:
        return render(request, 'borrowings.html', {
            'medias_borrowed': medias_borrowed,
            'borrowing_media_form':BorrowingMediaForm(),
            'return_media_form': return_borrowing_request,
            'anchor': 'return-media-section'
    })

@login_required
def borrowings(request):
    medias_borrowed = BorrowableMedia.objects.filter(is_available=False)
    for media in medias_borrowed:
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
    if request.method == 'POST':
        if 'submit_borrowing' in request.POST:
            return new_borrowing(request, medias_borrowed)
        elif 'submit_return' in request.POST:
            return return_borrowing(request, medias_borrowed)
    return render(request, 'borrowings.html', {
        'medias_borrowed': medias_borrowed,
        'borrowing_media_form': BorrowingMediaForm(),
        'return_media_form': ReturnMediaForm()
    })

def get_media_details_borrowing(request):
    media_id = request.GET.get('media_id')
    try:
        media = BorrowableMedia.objects.get(pk=media_id)
        if media.is_available == True:
            data = {'title': media.name}
            if hasattr(media, 'book'):
                data['author'] = media.book.author
            elif hasattr(media, 'cd'):
                data['author'] = media.cd.artist
            elif hasattr(media, 'dvd'):
                data['author'] = media.dvd.director
            else:
                data = {'error': "Ce type de média n'est pas reconnu"}
            return JsonResponse(data)
        else:
            data = {'error': 'Ce média est déjà emprunté par un membre'}
            return JsonResponse(data)
    except BorrowableMedia.DoesNotExist:
        data = {'error': 'Cet identifiant ne correspond à aucun média'}
        return JsonResponse(data)

def get_borrowed_media(request):
    member_id = request.GET.get('member_id')
    media_choices = []

    try:
        member = Member.objects.get(pk=member_id)
        member_data = {'name': f'{member.last_name} {member.first_name}'}
    except Member.DoesNotExist:
        data_error = {'error': 'Cet identifiant ne correspond à aucun membre'}
        return JsonResponse(data_error)

    medias = BorrowableMedia.objects.filter(borrower=member)
    for media in medias:
        media_choice = {
            'id': media.pk,
            'name': media.name,
            'borrowing_date': media.borrowing_date,
            'return_date': media.return_date
        }
        if hasattr(media, 'book'):
            media_choice['type'] = media.book.media_type
            media_choice['author'] = media.book.author
        elif hasattr(media, 'cd'):
            media_choice['type'] = media.cd.media_type
            media_choice['author'] = media.cd.artist
        elif hasattr(media, 'dvd'):
            media_choice['type'] = media.dvd.media_type
            media_choice['author'] = media.dvd.director
        else:
            media_choice['type'] = 'média non reconnu'
            media_choice['author'] = 'créateur inconnu'
        media_choices.append(media_choice)
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