"""
URL configuration for Myschool project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from users_auth import views, urls
from Myschool import settings

# added the static files to be able to load the files under the static folder
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("users_auth.urls")),
    path('accounts/', include('allauth.urls')),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
