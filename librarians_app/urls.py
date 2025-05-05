from django.urls import path
from librarians_app import views

urlpatterns = [
    path('gestion-des-medias/', views.media_management, name='media_management'),
    path('get-media-details-management/', views.get_media_details_management, name='get_media_details_management'),
    path('gestion-des-membres/', views.members_management, name='members_management'),
    path('get-member-details/', views.get_member_details, name='get_member_details'),
    path('emprunts/', views.borrowings, name='borrowings'),
    path('get-media-details-borrowing/', views.get_media_details_borrowing, name='get_media_details_borrowing'),
    path('get-borrowed-media/', views.get_borrowed_media, name='get_borrowed_media'),
]