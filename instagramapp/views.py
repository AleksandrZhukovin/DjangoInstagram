from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView, RedirectView
from .models import Post, Profile, Comment, Like, Message, Chat
from .forms import RegistrationForm, SearchForm, CommentForm
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.list import ListView


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        if user.is_authenticated:
            profile, created = Profile.objects.get_or_create(user=user)
        context['title'] = _('Profile {user}').format(user=user.username)
        context['user'] = user
        context['posts'] = Post.objects.filter(user=user)
        context['profile'] = Profile.objects.get(user=user)
        return context


class EditProfileView(UpdateView):
    model = Profile
    template_name = 'edit_profile.html'
    fields = ['status', 'location', 'image']
    success_url = reverse_lazy('profile')

    def get_initial(self):
        initial = super().get_initial()
        profile = Profile.objects.get(id=self.kwargs['pk'])
        initial['status'] = profile.status
        initial['location'] = profile.location
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['personal'] = False
        context['user'] = self.request.user
        return context


class EditProfilePersonalView(UpdateView):
    model = User
    template_name = 'edit_profile.html'
    fields = ['username', 'first_name', 'last_name', 'email']
    success_url = reverse_lazy('profile')

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['username'] = user.username
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        initial['email'] = user.email
        return initial


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
    success_url = reverse_lazy('home')

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
        current_user = self.request.user
        current_user_profile = Profile.objects.get(user=current_user)
        user = User.objects.get(id=self.kwargs['pk'])
        context['follow'] = False
        if user not in current_user_profile.following.all():
            context['follow'] = True
        context['title'] = user.username
        context['profile'] = Profile.objects.get(user=user)
        context['followers'] = len(Profile.objects.get(user=user).followers.all())
        context['following'] = len(Profile.objects.get(user=user).following.all())
        context['user'] = current_user
        context['posts'] = Post.objects.filter(user=user)
        return context


class FollowView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        current_user = self.request.user
        pk = self.kwargs['pk']
        current_user_profile = Profile.objects.get(user=current_user)
        current_user_profile.following.add(User.objects.get(id=pk))
        current_user_profile.save()
        f_user = Profile.objects.get(user=User.objects.get(id=pk))
        f_user.followers.add(current_user)
        f_user.save()
        self.url = '/user_profile{0}/'.format(pk)
        return super().get_redirect_url(*args, **kwargs)


class UnfollowView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        current_user = self.request.user
        pk = self.kwargs['pk']
        current_user_profile = Profile.objects.get(user=current_user)
        current_user_profile.following.remove(User.objects.get(id=pk))
        current_user_profile.save()
        f_user = Profile.objects.get(user=User.objects.get(id=pk))
        f_user.followers.remove(current_user)
        f_user.save()
        self.url = '/user_profile{0}/'.format(pk)
        return super().get_redirect_url(*args, **kwargs)


class PostView(CreateView):
    template_name = 'post.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        post = Post.objects.get(id=self.kwargs['pk'])
        comments = []
        n = 0
        for c in Comment.objects.filter(user=user):
            comments.append([c])
            comments[n].append([i.user for i in Like.objects.filter(user=user.id, comment=c)])
            comments[n].append(len(Like.objects.filter(comment=c)))
        context['comments'] = comments
        print(comments)
        likes = []
        for i in Like.objects.filter(post=post):
            likes.append(i.user)
        context['likes'] = likes
        context['like_amount'] = len(list(Like.objects.filter(post=post)))
        context['post'] = post

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return '/post{0}/'.format(self.kwargs['pk'])


class DeleteCommentView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment = Comment.objects.get(id=self.kwargs['pk'])
        comment.delete()
        self.url = '/post{0}/'.format(self.kwargs['post_id'])
        return super().get_redirect_url(*args, **kwargs)


class AddCommentLikeView(UpdateView):
    model = Comment

    def dispatch(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=self.kwargs['comment_id'])
        user = self.request.user
        like = Like(comment=comment, user=user)
        like.save()
        return redirect('/post{0}/'.format(self.kwargs['pk']))


class RemoveCommentLikeView(UpdateView):
    model = Comment

    def dispatch(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=self.kwargs['comment_id'])
        user = self.request.user
        like = Like.objects.get(comment=comment, user=user)
        like.delete()
        return redirect('/post{0}/'.format(self.kwargs['pk']))


class AddLikeView(UpdateView):
    model = Post

    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['pk'])
        user = self.request.user
        like = Like(post=post, user=user)
        like.save()
        return redirect('/post{0}/'.format(self.kwargs['pk']))


class RemoveLikeView(UpdateView):
    model = Post

    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['pk'])
        user = self.request.user
        like = Like.objects.get(post=post, user=user)
        like.delete()
        return redirect('/post{0}/'.format(self.kwargs['pk']))


class ChatView(CreateView):
    model = Message
    template_name = 'chat.html'
    fields = ['body']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.chat = Chat.objects.get(id=self.kwargs['chat'])
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(chat=self.kwargs['chat'])
        return context

    def get_success_url(self):
        return '/chat{0}'.format(self.kwargs['chat'])


class StartChatView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        user1 = User.objects.get(id=self.kwargs['user_id'])
        for c in Chat.objects.all():
            if user in c.members.all() and user1 in c.members.all():
                self.url = '/chat{0}'.format(c.id)
                break
        else:
            chat = Chat()
            chat.save()
            chat.members.add(user, user1)
            self.url = '/chat{0}'.format(chat.id)
        return super().get_redirect_url(*args, **kwargs)


class ChatsView(TemplateView):
    template_name = 'chats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chats = []
        for c in Chat.objects.all():
            if self.request.user in c.members.all():
                chats.append(c)
        context['chats'] = chats
        return context
