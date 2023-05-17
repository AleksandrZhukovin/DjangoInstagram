from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.HomeView.as_view()), name='home'),
    path('add_post/', login_required(views.AddPostView.as_view()), name='add_post'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('add_post/edit_post<int:pk>/', views.EditPostView.as_view(), name='edit_post'),
    path('post/<int:pk>/', views.PostView.as_view(), name='post_view')
]
