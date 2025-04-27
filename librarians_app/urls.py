from django.urls import path
from librarians_app import views

urlpatterns = [
    path('gestion-des-medias/', views.mediaManagement, name='media_management'),
    path('get-media-details-management/', views.getMediaDetailsManagement, name='get_media_details_management'),
    path('gestion-des-membres/', views.membersManagement, name='members_management'),
    path('get-member-details/', views.getMemberDetails, name='get_member_details'),
    path('emprunts/', views.borrowings, name='borrowings'),
    path('get-media-details-borrowing/', views.getMediaDetailsBorrowing, name='get_media_details_borrowing'),
    path('get-borrowed-media/', views.getBorrowedMedia, name='get_borrowed_media'),
]