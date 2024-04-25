"""
URL configuration for Myschool project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from users_auth import views, urls
from communication import views, urls
from usertasks import views, urls
from Myschool import settings

# added the static files to be able to load the files under the static folder
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("users_auth.urls")),
    path('communication/', include("communication.urls")),
    path('tasks/', include("usertasks.urls")),
    path('accounts/', include('allauth.urls')),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
