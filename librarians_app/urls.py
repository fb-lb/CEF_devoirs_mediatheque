from django.urls import path
from librarians_app import views

urlpatterns = [
    path('gestion-des-medias/', views.mediaManagement, name='media_management'),
    path('get-book-details/', views.getBookDetails, name='get_book_details'),
    path('emprunts/', views.borrowings, name='borrowings')
]