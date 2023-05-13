import datetime

import requests
import json
from tasks.models import Worker, Basics  # noqa


def send_message_bot(request):

    worker = Worker.objects.get(code=request['worker'])
    author = Worker.objects.get(code=request['author'])
    date = request['date'].replace("T", " ").replace("Z", "")
    base = Basics.objects.get(number=request['base'])

    message = f"""
    Задача номер {str(request['number'])} от {date}\n\n"{request['name']}"\n\nАвтор: { author }\nОснование: {base.name}
    """

    token = '5614919077:AAEaF1O3mJm-lNyP1fDD6-AXZnOYufB8FLw'

    url = 'https://api.telegram.org/bot' + token + '/sendMessage'

    reply_markup = {"inline_keyboard": [
                [{"text": "Выполнена", "callback_data": "done"}],
                [{"text": "Не выполнена", "callback_data": "dont"}],
                [{"text": "Переадресовать", "callback_data": "forward"}]
    ]}

    data = {'chat_id': worker.chat_id, 'text': message, 'reply_markup': json.dumps(reply_markup)}

    r = requests.post(url, data=data)

    return r.json()['ok']






