from django.urls import path, include
from mediatheque_app import views

urlpatterns = [
    path('', views.homepage),
    path('membres/', include("members_app.urls")),
]