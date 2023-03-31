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
    path('search/<str:search>/', views.SearchResultView.as_view(), name='search_res'),
    path('user_profile<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
    path('follow<int:pk>/', views.FollowView.as_view(), name='follow'),
    path('unfollow<int:pk>/', views.UnfollowView.as_view(), name='unfollow'),
    path('add_post/edit_post<int:pk>/', views.EditPostView.as_view(), name='edit_post'),
    path('post<int:pk>/', views.PostView.as_view(), name='post_view'),
    path('add_like<int:pk>/', views.AddLikeView.as_view(), name='add_like'),
    path('remove_like<int:pk>/', views.RemoveLikeView.as_view(), name='remove_like'),
    path('edit_profile<int:pk>/', views.EditProfileView.as_view(), name='edit_profile'),
    path('edit_profile_personal<int:pk>/', views.EditProfilePersonalView.as_view(), name='edit_profile_personal'),
    path('delete_comment<int:pk>/<int:post_id>/', views.DeleteCommentView.as_view(), name='delete_comment'),
    path('add_comment_like<int:pk>/<int:comment_id>/', views.AddCommentLikeView.as_view(), name='add_comment_like'),
    path('remove_comment_like<int:pk>/<int:comment_id>/', views.RemoveCommentLikeView.as_view(), name='remove_comment_like')
]
