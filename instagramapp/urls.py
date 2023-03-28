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
    path('search/<str:search>/', views.SearchResultView.as_view(), name='search_res')
]
