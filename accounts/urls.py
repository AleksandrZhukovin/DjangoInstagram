from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('profile/', login_required(views.ProfileView.as_view()), name='profile'),
    path('edit_profile/<int:pk>/', views.EditProfileView.as_view(), name='edit_profile'),
    path('edit_profile_personal/<int:pk>/', views.EditProfilePersonalView.as_view(), name='edit_profile_personal'),
    path('user_profile/<int:pk>/', views.UserProfileView.as_view(), name='user_profile')
]
