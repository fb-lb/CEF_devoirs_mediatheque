from django.urls import path
from librarians_app import views

urlpatterns = [
    path('gestion-des-medias/', views.mediaManagement, name='media_management'),
    path('get-book-details/', views.getBookDetails, name='get_book_details'),
    path('gestion-des-membres/', views.membersManagement, name='members_management'),
    path('get-member-details/', views.getMemberDetails, name='get_member_details'),
    path('emprunts/', views.borrowings, name='borrowings'),
    path('get-media-details/', views.getMediaDetails, name='get_media_details'),
    path('get-borrowed-media/', views.getBorrowedMedia, name='get_borrowed_media'),
]