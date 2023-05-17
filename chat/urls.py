from django.urls import path
from . import views

urlpatterns = [
    path('start_chat/<int:user_id>/', views.StartChatView.as_view(), name='start_chat'),
    path('chats/', views.ChatsView.as_view(), name='chats')
]
