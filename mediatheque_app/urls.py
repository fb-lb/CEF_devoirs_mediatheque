from django.urls import path, include
from django.contrib import admin
from mediatheque_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='home_page'),
    path('admin/', admin.site.urls),
    path('membres/', include("members_app.urls")),
    path('bibliothecaire/', include("librarians_app.urls"))
]
'''
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    '''