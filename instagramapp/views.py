from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from .models import Post, Profile
from .forms import RegistrationForm, ProfileEdit
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.list import ListView


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['title'] = _('Profile {user}').format(user=user.username)
        context['user'] = user
        context['posts'] = Post.objects.filter(user=user)
        context['profile'] = Profile.objects.get(user=user)
        return context


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Sign Up')
        return context


class Login(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    extra_context = {'title': _('Log In')}


class Logout(LogoutView):
    pass


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
