from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('profile/', login_required(views.ProfileView.as_view()), name='profile'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('user_profile/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
    path('personal_info/', views.EditProfilePersonalView.as_view(), name='edit_personal'),
    path('security/', views.EditSecurityView.as_view(), name='edit_security'),
    path('notifications/', views.EditNotificationsView.as_view(), name='edit_notifications'),
    path('profile_info/', views.ProfileInfoView.as_view(), name='profile_info')
]
