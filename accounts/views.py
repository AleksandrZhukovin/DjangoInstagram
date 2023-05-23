from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from accounts.models import User, Follow
from instagramapp.models import Post
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .forms import EditProfileForm


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        follow = Follow.objects.get(user=user)
        context = super().get_context_data(**kwargs)
        context['title'] = _('Profile {user}').format(user=user.username)
        context['user'] = user
        context['posts'] = Post.objects.filter(user=user)
        context['post_am'] = len(Post.objects.filter(user=user))
        context['followers'] = len(follow.followers.all())
        context['following'] = len(follow.following.all())
        return context


class EditProfileView(UpdateView):
    model = User
    template_name = 'edit_profile.html'
    fields = ['status', 'image']
    success_url = reverse_lazy('profile')

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['status'] = user.status
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


class UserProfileView(TemplateView):
    template_name = 'user_profile.html'

    def post(self, request, **kwargs):
        data_post = request.POST
        current_user = self.request.user
        current_user_follow = Follow.objects.get(user=current_user)
        f_user = Follow.objects.get(user=User.objects.get(id=data_post['follow']))
        if data_post['is_followed'] == '0':
            current_user_follow.following.add(User.objects.get(id=data_post['follow']))
            current_user_follow.save()
            f_user.followers.add(current_user)
            f_user.save()
            return JsonResponse({'is_follow': 1, 'followers': len(f_user.followers.all())})
        else:
            current_user_follow.following.remove(User.objects.get(id=data_post['follow']))
            current_user_follow.save()
            f_user.followers.remove(current_user)
            f_user.save()
            return JsonResponse({'is_follow': 0, 'followers': len(f_user.followers.all())})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        current_user_follow = Follow.objects.get(user=current_user)
        user = User.objects.get(id=self.kwargs['pk'])
        context['is_followed'] = 1
        if user not in current_user_follow.following.all():
            context['is_followed'] = 0
        context['title'] = user.username
        context['followers'] = len(current_user_follow.followers.all())
        context['following'] = len(current_user_follow.following.all())
        context['current_user'] = current_user
        context['user'] = user
        context['posts'] = Post.objects.filter(user=user)
        context['post_am'] = len(Post.objects.filter(user=user))
        return context


__all__ = ['ProfileView', 'EditProfileView', 'UserProfileView', 'EditProfilePersonalView']
