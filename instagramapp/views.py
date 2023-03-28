from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from .models import Post, Profile
from .forms import RegistrationForm, ProfileEdit, SearchForm
from django.views.generic.edit import CreateView, UpdateView, FormView
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

    def form_valid(self, form):
        profile = Profile(user=self.request.user)
        profile.save()
        return super().form_valid(form)


class Login(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    extra_context = {'title': _('Log In')}


class Logout(LogoutView):
    pass


class HomeView(ListView):
    model = Post
    template_name = 'home.html'


class AddPostView(CreateView):
    model = Post
    template_name = 'add_post.html'
    fields = ['image']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return f'edit_post{self.object.id}/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Add Post')
        return context


class EditPostView(UpdateView):
    model = Post
    template_name = 'add_post.html'
    fields = ['image', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Add Post')
        context['post'] = Post.objects.get(id=self.kwargs['pk'])
        return context


class SearchView(FormView):
    model = User
    template_name = 'search.html'
    form_class = SearchForm
    search = ''

    def form_valid(self, form):
        self.search = form.cleaned_data['search']
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Search')
        return context

    def get_success_url(self):
        return '/search/{0}/'.format(self.search)


class SearchResultView(SearchView):
    def get_initial(self):
        initial = super().get_initial()
        initial['search'] = self.kwargs['search']
        return initial

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['results'] = User.objects.filter(username__contains=self.kwargs['search'])
        return context


class UserProfileView(TemplateView):
    template_name = 'user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['pk'])
        context['title'] = user.username
        context['profile'] = Profile.objects.get(user=user)
        return context
