from django.urls import path

from send_message.views import send_message_temp, send_message

urlpatterns = [
    path('', send_message_temp, name='send_mess_temp'),
    path('send', send_message, name='send_message')
]
