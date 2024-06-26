from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# from send_message.services import send_message_to_telegram
from core.tasks import send_message_to_telegram
from tasks.models import Worker

# Create your views here.


@login_required
def send_message_temp(request):
    trades_list = Worker.objects.filter(chat_id__isnull=False)
    context = {'trades_list': trades_list}
    return render(request, 'messages/send_message.html', context=context)


def send_message(request):
    trades_list = request.POST.getlist('trades_list')
    message = request.POST.get('message')
    send_message_to_telegram.delay(trades_list, message)
    # send_message_to_telegram(trades_list, message)
    return HttpResponse('<h1>OK</h1>')
