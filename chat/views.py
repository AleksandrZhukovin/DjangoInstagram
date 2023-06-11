from chat.models import Chat, Message
from django.http import JsonResponse
from accounts.models import User
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView, RedirectView
from .forms import ChatForm
from django.template.loader import render_to_string


class StartChatView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        user1 = User.objects.get(id=self.kwargs['user_id'])
        for c in Chat.objects.all():
            if user in c.members.all() and user1 in c.members.all():
                self.url = '/chats'
                break
        else:
            chat = Chat()
            chat.save()
            chat.members.add(user, user1)
            self.url = '/chats'
        return super().get_redirect_url(*args, **kwargs)


class ChatsView(TemplateView):
    template_name = 'chats.html'

    def post(self, request):
        data_post = request.POST
        user = self.request.user
        chat = Chat.objects.get(id=data_post['chat'])
        if 'message' in data_post.keys():
            message = Message(user=user, chat=chat, body=data_post['message'])
            message.save()
            return JsonResponse({'message': message.body}, safe=False)
        messages = Message.objects.filter(chat=chat)
        form = ChatForm()
        result = render_to_string('chat.html', {'messages': messages, 'form': form, 'chat': chat, 'user': user})
        return JsonResponse(result, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        chats = []
        for c in Chat.objects.all():
            if user in c.members.all():
                for u in c.members.all():
                    if u != user:
                        chats.append([c, u])
        context['profile'] = user
        context['chats'] = chats
        context['title'] = _('Chat')
        return context


__all__ = ['ChatsView', 'StartChatView']
