from django.urls import path, include
from django.contrib import admin
from mediatheque_app import views

urlpatterns = [
    path('', views.homepage, name='home_page'),
    path('admin/', admin.site.urls),
    path('membres/', include("members_app.urls")),
    path('bibliothecaire/', include("librarians_app.urls"))
]