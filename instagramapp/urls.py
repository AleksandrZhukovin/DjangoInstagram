from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.HomeView.as_view()), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('add_post/', views.AddPostView.as_view(), name='add_post'),
    path('post/<int:pk>/', views.PostView.as_view(), name='post_view')
]
