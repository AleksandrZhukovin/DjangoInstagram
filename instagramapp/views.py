from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from models import Post, Profile


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
