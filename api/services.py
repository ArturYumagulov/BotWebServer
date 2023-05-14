import datetime
import environ

import requests
import json
from tasks.models import Worker, Basics, AuthorComments, WorkerComments  # noqa

env = environ.Env()
environ.Env.read_env()


def send_message_bot(request):

    worker = Worker.objects.get(code=request['worker'])
    author = Worker.objects.get(code=request['author'])
    date = request['date'].replace("T", " ").replace("Z", "")
    base = Basics.objects.get(number=request['base'])
    author_comment = AuthorComments.objects.get(id=request['author_comment'])
    worker_comment = WorkerComments.objects.get(id=request['worker_comment'])

    if request['status'] == 'Переадресована':
        task_header = {'text': "Вам переадресована задача"}
    else:
        task_header = {'text': "Задача"}

    message = f"""
    
    {task_header['text']} номер {str(request['number'])} от {date}\n\n"{request['name']}"\n\nОснование: {base.name}\n\nАвтор: { author }\n\nКомментарий автора: {author_comment.comment}\n"""

    sub_text = f"Комментарий исполнителя:\n {worker_comment.comment}"

    if worker_comment.id != 34:
        message += sub_text

    token = env.str("BOT_TOKEN")

    url = 'https://api.telegram.org/bot' + token + '/sendMessage'

    reply_markup = {"inline_keyboard": [
                [{"text": "Выполнена ✅", "callback_data": f"done_{request['number']}"}],
                [{"text": "Не выполнена ❌", "callback_data": f"dont_{request['number']}"}],
                [{"text": "Переадресовать ↪️", "callback_data": f"first_forward_{request['number']}"}]
    ]}

    data = {'chat_id': worker.chat_id, 'text': message, 'reply_markup': json.dumps(reply_markup)}

    r = requests.post(url, data=data)

    return r.json()['ok']


if __name__ == '__main__':
    print(env("BOT_TOKEN"))
    pass


