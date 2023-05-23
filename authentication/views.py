from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView
from .forms import RegistrationForm, LoginForm


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


__all__ = ['Logout', 'Login', 'RegistrationView']
