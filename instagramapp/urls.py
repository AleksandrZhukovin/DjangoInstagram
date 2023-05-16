from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.HomeView.as_view()), name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('profile/', login_required(views.ProfileView.as_view()), name='profile'),
    path('add_post/', login_required(views.AddPostView.as_view()), name='add_post'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('user_profile<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
    path('add_post/edit_post<int:pk>/', views.EditPostView.as_view(), name='edit_post'),
    path('post<int:pk>/', views.PostView.as_view(), name='post_view'),
    path('edit_profile<int:pk>/', views.EditProfileView.as_view(), name='edit_profile'),
    path('edit_profile_personal<int:pk>/', views.EditProfilePersonalView.as_view(), name='edit_profile_personal'),
    path('start_chat<int:user_id>/', views.StartChatView.as_view(), name='start_chat'),
    path('chats/', views.ChatsView.as_view(), name='chats')
]
