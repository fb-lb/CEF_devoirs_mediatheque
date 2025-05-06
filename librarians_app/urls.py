from django.urls import path
from django.contrib.auth import views as auth_views
from librarians_app import views
from librarians_app.forms import LoginForm

urlpatterns = [
    path('connexion/', auth_views.LoginView.as_view(template_name="login.html", authentication_form=LoginForm), name='login'),
    path('deconnexion/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('gestion-des-medias/', views.media_management, name='media_management'),
    path('get-media-details-management/', views.get_media_details_management, name='get_media_details_management'),
    path('gestion-des-membres/', views.members_management, name='members_management'),
    path('get-member-details/', views.get_member_details, name='get_member_details'),
    path('emprunts/', views.borrowings, name='borrowings'),
    path('get-media-details-borrowing/', views.get_media_details_borrowing, name='get_media_details_borrowing'),
    path('get-borrowed-media/', views.get_borrowed_media, name='get_borrowed_media'),
]