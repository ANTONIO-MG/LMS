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
from users_auth.views import password_reset_from_key


# added the static files to be able to load the files under the static folder
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("users_auth.urls")),
    path('', include("communication.urls")),
    path('', include("usertasks.urls")),
    path('accounts/', include('allauth.urls')),
    path('accounts/password/reset/key/<uidb36>-<key>/', password_reset_from_key, name='account_reset_password_from_key')

    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
