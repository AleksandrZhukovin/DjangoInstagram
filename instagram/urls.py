from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('instagramapp.urls')),
    path('', include('chat.urls')),
    path('', include('authentication.urls')),
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),
]
