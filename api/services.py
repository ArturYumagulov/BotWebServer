import environ

import requests
import json
from tasks.models import Worker, Basics, AuthorComments, WorkerComments, Partner  # noqa

env = environ.Env()
environ.Env.read_env()


def send_message_bot(request):

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

    reply_markup = {"inline_keyboard": [
                [{"text": "Выполнена ✅", "callback_data": f"ok_{request['number']}"}],
                [{"text": "Отклонить ❌", "callback_data": f"dont_{request['number']}"}],
                [{"text": "Переадресовать ↪️", "callback_data": f"first_forward_{request['number']}"}]
    ]}

    sub_text = f"Комментарий исполнителя: \n {worker_comment.comment}"

    if request['status'] == 'Новая':
        task_header = {'text': "Задача"}
        message = f"{task_header['text']} от " \
                  f"{date}\n\n" \
                  f"'{request['name']}'\n\n" \
                  f"Исполнить до:\n" \
                  f"{deadline}\n\n" \
                  f"Автор:\n" \
                  f"{author}\n\n" \
                  f"Контрагент:\n" \
                  f"{partner.name}\n\n" \
                  f"Основание:\n" \
                  f"{base.name}\n\n" \
                  f"Комментарий автора:\n" \
                  f"{author_comment.comment}\n"

        if worker_comment.id != 1:
            message += sub_text

        data = {'chat_id': worker.chat_id, 'text': message, 'reply_markup': json.dumps(reply_markup)}

        r = requests.post(url, data=data)

        return True

    if request['status'] == 'Переадресована':
        task_header = {'text': "Вам переадресована задача"}
        message = f"{task_header['text']} от " \
                  f"{date}\n\n" \
                  f"'{request['name']}'\n\n" \
                  f"Исполнить до:\n" \
                  f"{deadline}\n\n" \
                  f"Автор:\n" \
                  f"{author}\n\n" \
                  f"Контрагент:\n" \
                  f"{partner.name}\n\n" \
                  f"Основание:\n" \
                  f"{base.name}\n\n" \
                  f"Комментарий автора:\n" \
                  f"{author_comment.comment}\n"

        if worker_comment.id != 1:
            message += sub_text

        data = {'chat_id': worker.chat_id, 'text': message, 'reply_markup': json.dumps(reply_markup)}

        r = requests.post(url, data=data)

        return True

    elif request['status'] == "Отклонена":
        task_header = {'text': "Отклонена задача"}
        message = f"{task_header['text']} от " \
                  f"{date}\n\n" \
                  f"'{request['name']}'\n\n" \
                  f"Исполнить до:\n" \
                  f"{deadline}\n\n" \
                  f"Автор:\n" \
                  f"{author}\n\n" \
                  f"Контрагент:\n" \
                  f"{partner.name}\n\n" \
                  f"Основание:\n" \
                  f"{base.name}\n\n" \
                  f"Комментарий автора:\n" \
                  f"{author_comment.comment}\n"

        if worker_comment.id != 1:
            message += sub_text

        data = {'chat_id': author.chat_id, 'text': message}

        r = requests.post(url, data=data)

        return True

    else:
        return False


if __name__ == '__main__':
    pass


