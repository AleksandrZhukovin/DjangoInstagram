from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from accounts.models import User, Follow
from instagramapp.models import Post
from pathlib import Path
from django.core.files import File
from .forms import EditProfileForm, EditProfilePersonalForm, EditSecurityForm, EditNotificationsForm
from django.db.utils import IntegrityError


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


class EditProfileView(TemplateView):
    template_name = 'edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['form'] = EditProfileForm()
        context['header'] = 'Edit Profile'
        context['url'] = '/edit_profile/'
        return context

    def post(self, request):
        user = self.request.user
        data = request.POST
        if 'bio' in data.keys():
            if 'file' in request.FILES.keys():
                data_f = request.FILES['file']
                with open('instagram/static/images/upload_image.png', 'wb') as file:
                    file.write(data_f.read())
                path = Path(f'instagram/static/images/upload_image.png')
                with path.open(mode='rb') as f:
                    file = File(f, name=path.name)
                    user_mod = User.objects.get(id=user.id)
                    user_mod.image = file
                    user_mod.bio = data['bio']
                    user_mod.gender = data['gender']
                    user_mod.website = data['website']
                    user_mod.save()
                    response = {'bio': user_mod.bio, 'gender': user_mod.gender, 'website': user_mod.website,
                                'image': '/static/images/upload_image.png'}
                    return JsonResponse(response, safe=False)
            else:
                user_mod = User.objects.get(id=user.id)
                user_mod.bio = data['bio']
                user_mod.gender = data['gender']
                user_mod.website = data['website']
                user_mod.save()
                response = {'bio': user_mod.bio, 'gender': user_mod.gender, 'website': user_mod.website}
                return JsonResponse(response, safe=False)
        if len(data.keys()) == 1:
            response = {'bio': user.bio, 'gender': user.gender, 'website': user.website, 'select': 'profile'}
            return JsonResponse(response, safe=False)


class EditProfilePersonalView(TemplateView):
    template_name = 'edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['form'] = EditProfilePersonalForm()
        context['header'] = 'Personal'
        context['url'] = '/personal_info/'
        return context

    def post(self, request):
        user = self.request.user
        data = request.POST
        if len(data.keys()) == 1:
            response = {'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name,
                        'select': 'personal'}
            return JsonResponse(response, safe=False)
        else:
            user_mod = User.objects.get(id=user.id)
            user_mod.username = data['username']
            user_mod.first_name = data['first_name']
            user_mod.last_name = data['last_name']
            try:
                user_mod.save()
            except IntegrityError:
                return JsonResponse({'error': 'Username already exists!'}, safe=False)
            response = {'username': user_mod.username, 'first_name': user_mod.first_name, 'last_name': user_mod.last_name,
                        'select': 'personal'}
            return JsonResponse(response, safe=False)


class EditSecurityView(TemplateView):
    template_name = 'edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['form'] = EditSecurityForm()
        context['header'] = 'Security'
        context['url'] = '/security/'
        return context


class EditNotificationsView(TemplateView):
    template_name = 'edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['form'] = EditNotificationsForm()
        context['header'] = 'Notifications'
        context['url'] = '/notifications/'
        return context

    def post(self, request):
        user = self.request.user
        data = request.POST
        if len(data.keys()) == 1:
            response = {'email': user.email, 'select': 'notifications'}
            return JsonResponse(response, safe=False)
        else:
            user_mod = User.objects.get(id=user.id)
            user_mod.email = data['email']
            try:
                user_mod.save()
            except IntegrityError:
                return JsonResponse({'error': 'There is already an account with such email!'}, safe=False)
            response = {'email': user_mod.email, 'select': 'personal'}
            return JsonResponse(response, safe=False)


class ProfileInfoView(TemplateView):
    template_name = 'edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['header'] = 'Profile Info'
        context['session_time'] = self.request.user.date_joined.strftime('%d.%m.%Y at %H:%M:%S')
        context['url'] = '/profile_info/'
        return context


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
