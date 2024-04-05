import environ

import requests
import json
from tasks.models import Worker, Basics, AuthorComments, WorkerComments, Partner, Task, ResultGroup  # noqa

env = environ.Env()
environ.Env.read_env('BotWebServer/.env')


def send_message_bot(request):
    task = Task.objects.get(number=request['number'])
    worker = Worker.objects.get(code=request['worker'])
    author = Worker.objects.get(code=request['author'])
    partner = Partner.objects.get(code=request['partner'])
    date = request['date'].replace("T", " ").replace("Z", "")
    deadline = request['deadline'].replace("T", " ").replace("Z", "")
    base = Basics.objects.get(number=request['base'])
    author_comment = AuthorComments.objects.get(id=request['author_comment'])
    worker_comment = WorkerComments.objects.get(id=request['worker_comment'])

    token = env.str("BOT_TOKEN")
    url = 'https://api.telegram.org/bot' + token + '/sendMessage'
    group_name = base.group.name
    task_header = {'text': "Задача"}
    sub_text = f"<b>Комментарий исполнителя:</b> \n" \
               f"{worker_comment.comment}"

    if base.group.code == ResultGroup.objects.get(name="Сенсус").code:  # Если "Разработка контрагента"

        author_comment_clean = author_comment.comment.split('_')[0]
        link_url = author_comment.comment.split('_')[1]

        message = f"{task_header['text']} от " \
                  f"{date}\n\n" \
                  f"Cенсус по адресу: '{task.name}'\n\n" \
                  f"<b>Исполнить до:</b>\n" \
                  f"{deadline}\n" \
                  f"<b>Автор:</b>\n" \
                  f"{author}\n" \
                  f"<b>Контрагент:</b>\n" \
                  f"{partner.name}\n" \
                  f"<b>Основание:</b>\n" \
                  f"{base.name}\n\n" \
                  f"<b>Комментарий автора:</b>\n" \
                  f"{author_comment_clean}\n"

        if worker_comment.id != 2:
            message += sub_text

        reply_markup = {"inline_keyboard": [
                    [{"text": "Сенсус", "url": link_url}],
                    [{"text": "Переадресовать ↪️", "callback_data": f"first_forward_{request['number']}"}]
        ]}

    elif base.group.code == ResultGroup.objects.get(name="Кредитный Контроль").code:  # Если "Кредитный Контроль"

        message = f"{task_header['text']} от " \
                  f"{date}\n\n" \
                  f"'{group_name}'\n\n" \
                  f"<b>Исполнить до:</b>\n" \
                  f"{deadline}\n" \
                  f"<b>Автор:</b>\n" \
                  f"{author}\n" \
                  f"<b>Контрагент:</b>\n" \
                  f"{partner.name}\n" \
                  f"<b>Основание:</b>\n" \
                  f"{base.name}\n\n" \
                  f"<b>Комментарий автора:</b>\n" \
                  f"{author_comment.comment}\n"

        if worker_comment.id != 2:
            message += sub_text

        if author.code == "HardCollect":
            reply_markup = {"inline_keyboard": [
                [{"text": "Выполнена", "callback_data": f"ok_{request['number']}"}],  # ✅
            ]}
        else:
            reply_markup = {"inline_keyboard": [
                [{"text": "Выполнена", "callback_data": f"ok_{request['number']}"}],  # ✅
                [{"text": "Переадресовать", "callback_data": f"first_forward_{request['number']}"}]  # ↪️
            ]}

    data = {'chat_id': worker.chat_id, 'text': message, 'reply_markup': json.dumps(reply_markup),
            'parse_mode': "HTML"}

    r = requests.post(url, data=data)

    if r.json()['ok']:
        task.message_id = r.json()['result']['message_id']
        task.save()
        return {'result': True, 'description': r.json()}
    else:
        return {'result': False, 'description': {'chat_id': worker.chat_id, 'description': r.json()}}


if __name__ == '__main__':
    pass
