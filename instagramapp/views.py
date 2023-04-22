from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView, RedirectView
from .models import Post, Profile, Comment, Like, Message, Chat
from .forms import RegistrationForm, SearchForm, CommentForm, AddPostForm, EditPostForm, LoginForm, EditProfileForm, \
    ChatForm
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.contrib.auth.views import LoginView, LogoutView


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        context = super().get_context_data(**kwargs)
        context['title'] = _('Profile {user}').format(user=user.username)
        context['user'] = user
        context['posts'] = Post.objects.filter(user=user)
        context['post_am'] = len(Post.objects.filter(user=user))
        context['profile'] = profile
        context['followers'] = len(profile.followers.all())
        context['following'] = len(profile.following.all())
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
    form_class = EditProfileForm
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
    form_class = LoginForm


class Logout(LogoutView):
    pass


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = None
        if user.is_authenticated:
            profile, created = Profile.objects.get_or_create(user=user)
        posts = Post.objects.all()
        wall = []
        for p in posts:
            if p.user in profile.following.all():
                likes = []
                for l in Like.objects.filter(post=p):
                    likes.append(l.user)
                wall.append([p, likes, len(likes)])
        context['posts'] = wall
        context['title'] = _('Home')
        context['user'] = user
        context['profile'] = profile
        return context


class AddPostView(CreateView):
    model = Post
    template_name = 'add_post.html'
    form_class = AddPostForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.instance.profile = Profile.objects.get(user=user)
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
    form_class = EditPostForm
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
        context['profile'] = Profile.objects.get(user=self.request.user)
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
        users = User.objects.filter(username__contains=self.kwargs['search'])
        profiles = []
        for u in users:
            profiles.append(Profile.objects.get(user=u))
        context['results'] = profiles
        context['profile'] = Profile.objects.get(user=self.request.user)
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
        context['post_am'] = len(Post.objects.filter(user=user))
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

    def post(self, request, *args, **kwargs):
        post_data = request.POST
        post = Post.objects.get(id=self.kwargs['pk'])
        user = self.request.user
        profile = Profile.objects.get(user=user)
        cookie = request.COOKIES.get('like'+str(post.id))
        if cookie == '1' and 'add_like' in post_data.keys():
            like = Like.objects.get(user=user, post=post)
            like.delete()
        elif 'add_like' in post_data.keys():
            like = Like(post=post, user=user)
            like.save()
        if 'body' in post_data.keys():
            comment = Comment(body=post_data['body'], user=user, profile=profile, post=post)
            comment.save()
            comment_info = {'user': user, 'profile': profile,
                            'like_am': 0, 'post': post, 'comment': comment}
            block = render_to_string('comment_template.html', comment_info)
            return JsonResponse(block, safe=False)
        if 'delete_comment' in post_data.keys():
            comment = Comment.objects.get(id=int(post_data['delete_comment']))
            comment_id = comment.id
            comment.delete()
            data = {'id': comment_id}
            return JsonResponse(data, safe=False)
        if 'like_comment' in post_data.keys():
            try:
                comment = Comment.objects.get(id=int(post_data['like_comment']))
                like = Like.objects.get(user=user, comment=comment)
                like.delete()
                data = {'like_am': len(Like.objects.filter(comment=comment)), 'id': comment.id, 'is_liked': 0}
                return JsonResponse(data, safe=False)
            except Like.DoesNotExist:
                comment = Comment.objects.get(id=int(post_data['like_comment']))
                like = Like(comment=comment, user=user)
                like.save()
                data = {'like_am': len(Like.objects.filter(comment=comment)), 'id': comment.id, 'is_liked': 1}
                return JsonResponse(data, safe=False)
        data = {'status': 'success', 'like_amount': len(Like.objects.filter(post=post))}
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        post = Post.objects.get(id=self.kwargs['pk'])
        comments = []
        n = 0
        for c in Comment.objects.filter(user=user, post=post):
            comments.append([c])
            try:
                Like.objects.get(comment=c, user=user)
                comments[n].append(1)
            except Like.DoesNotExist:
                comments[n].append(0)
            comments[n].append(len(Like.objects.filter(comment=c)))
            n += 1
        context['comments'] = comments
        likes = []
        for i in Like.objects.filter(post=post):
            likes.append(i.user)
        context['likes'] = likes
        context['like_amount'] = len(Like.objects.filter(post=post))
        context['post'] = post
        context['title'] = _('Post')
        context['profile'] = Profile.objects.get(user=post.user)
        return context


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


class ChatView(CreateView):
    model = Message
    template_name = 'chat.html'
    form_class = ChatForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.chat = Chat.objects.get(id=self.kwargs['chat'])
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(chat=self.kwargs['chat'])
        context['user'] = self.request.user
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
        user = self.request.user
        chats = []
        for c in Chat.objects.all():
            if user in c.members.all():
                for u in c.members.all():
                    if u != user:
                        chats.append([c, Profile.objects.get(user=u)])
        context['profile'] = Profile.objects.get(user=user)
        context['chats'] = chats
        return context
