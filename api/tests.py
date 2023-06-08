from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from tasks import models

User = get_user_model()

ROUTES = {
    'base': '/api/v1/base/',
    'partners': "/api/v1/partners/",
    'partner_worker': '/api/v1/partners-worker/',
    'supervisor': '/api/v1/supervisors/',
    'workers': '/api/v1/workers/',
    'author_comment': '/api/v1/author_comment/',
    'worker_comment': '/api/v1/worker_comment/',
    'auth': '/api/v1/token-auth/',
    'auth_data': {'username': "test_user", 'password': "test12345"}
}


class BaseTests(APITestCase):
    """Тестирование оснований"""

    base_url = ROUTES['base']
    model = models.Basics

    create_data = [
        {
            "number": "00000142871",
            "name": "Событие 00000142871 от 05.06.2023 16:37:47",
            "date": "2023-06-05T16:37:47Z"
        },
        {
            "number": "00000142866",
            "name": "Событие 00000142866 от 02.06.2023 16:59:07",
            "date": "2023-06-02T16:59:07Z"
        },
        {
            "number": "00000142865",
            "name": "Событие 00000142865 от 02.06.2023 15:34:20",
            "date": "2023-06-02T15:34:20Z"
        }
    ]

    update_data = [
        {
            "number": "00000142871",
            "name": "Изменено",
            "date": "2023-06-05T16:37:47Z"
        }
    ]
    error_data = {
            "number": "00000142871",
            "name": "Изменено",
            "date": "2023-06-05T16:37:47Z"
        }

    def setUp(self):
        self.client = APIClient()
        self.is_authenticated = User.objects.create_user(
            username=ROUTES['auth_data']['username'],
            password=ROUTES['auth_data']['password'])
        self.response = self.client.post(ROUTES['auth'], data=ROUTES['auth_data'])
        self.token = Token.objects.get(user__username=ROUTES['auth_data']['username'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_and_update_basic(self):
        create_response = self.client.post(self.base_url, self.create_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.model.objects.count(), 3)
        update_response = self.client.put(self.base_url, self.update_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.model.objects.get(number=self.update_data[0]['number']).name, self.update_data[0]['name'])

    def test_error_list_data(self):
        error_update_post = self.client.post(self.base_url, self.error_data, format='json')
        self.assertEqual(error_update_post.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


class PartnersTests(APITestCase):

    base_url = ROUTES['partners']
    partner_worker_url = ROUTES['partner_worker']
    model = models.Partner
    worker_model = models.PartnerWorker

    create_data = [
        {
            "code": "ТСО007316",
            "name": "Авангард-Моторс ООО"
        },
        {
            "code": "ТСО017919",
            "name": "Авзалова Эльза Илгизовна ИП"
        },
        {
            "code": "ТСО007244",
            "name": "АВТОХИМГРУПП ООО ТД"
        }
    ]

    update_data = [
        {
            "code": "ТСО007316",
            "name": "Изменено"
        }
    ]
    error_data = {
            "number": "00000142871",
            "name": "Изменено",
            "date": "2023-06-05T16:37:47Z"
        }

    partner_worker_data = [
        {
            "name": "Ильясов Ренат  Мирзанурович",
            "positions": "Директор",
            "code": "F00001716",
            "partner": "ТСО007316"
        },
        {
            "name": "Сотрулник 2",
            "positions": "Директор",
            "code": "F00001716",
            "partner": "ТСО017919"
        }

    ]

    def setUp(self):
        self.client = APIClient()
        self.is_authenticated = User.objects.create_user(
            username=ROUTES['auth_data']['username'],
            password=ROUTES['auth_data']['password'])
        self.response = self.client.post(ROUTES['auth'], data=ROUTES['auth_data'])
        self.token = Token.objects.get(user__username=ROUTES['auth_data']['username'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_and_update_partners(self):
        create_response = self.client.post(self.base_url, self.create_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.model.objects.count(), 3)
        update_response = self.client.put(self.base_url, self.update_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.model.objects.get(code=self.update_data[0]['code']).name, self.update_data[0]['name'])
        create_worker_response = self.client.post(self.partner_worker_url, data=self.partner_worker_data, format='json')
        self.assertEqual(create_worker_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.worker_model.objects.count(), 2)

    def test_error_list_partners(self):
        error_update_post = self.client.post(self.base_url, self.error_data, format='json')
        self.assertEqual(error_update_post.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        error_update_post = self.client.post(self.partner_worker_url, self.error_data, format='json')
        self.assertEqual(error_update_post.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


class SupervisorsWorkerTests(APITestCase):

    supervisor_url = ROUTES['supervisor']
    worker_url = ROUTES['workers']
    supervisor_model = models.Supervisor
    worker_model = models.Worker

    create_data = [
        {
            "code": "ТСО001951",
            "name": "Алтынбаев Артур Фаридович",
            "chat_id": None,
            "phone": "79655820336"
        },
        {
            "code": "ТСО000780",
            "name": "Габитов Ильнар Салимуллович",
            "chat_id": None,
            "phone": "79600847615"
        },
        {
            "code": "ТСО012297",
            "name": "Галеев Рамиль Мухаметшакирович",
            "chat_id": None,
            "phone": "79173908880"
        }
    ]

    update_data = [
        {
            "code": "ТСО000780",
            "name": "Изменено",
            "chat_id": None,
            "phone": "79600847615"
        }
    ]
    error_data = {
            "number": "00000142871",
            "name": "Изменено",
            "date": "2023-06-05T16:37:47Z"
        }

    worker_data = [
        {
            "code": "ТСО001099",
            "name": "Trade 10",
            "chat_id": None,
            "phone": "79677708030",
            "controller": False,
            "supervisor": "ТСО001951"
        },
        {
            "code": "ТСО001097",
            "name": "Trade 11",
            "chat_id": None,
            "phone": "79172961358",
            "controller": False,
            "supervisor": "ТСО001951"
        }

    ]

    def setUp(self):
        self.client = APIClient()
        self.is_authenticated = User.objects.create_user(
            username=ROUTES['auth_data']['username'],
            password=ROUTES['auth_data']['password'])
        self.response = self.client.post(ROUTES['auth'], data=ROUTES['auth_data'])
        self.token = Token.objects.get(user__username=ROUTES['auth_data']['username'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_and_update_supervisors_workers(self):
        create_response = self.client.post(self.supervisor_url, self.create_data, format='json')

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.supervisor_model.objects.count(), 3)

        update_response = self.client.put(self.supervisor_url, self.update_data, format='json')

        self.assertEqual(update_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.supervisor_model.objects.get(code=self.update_data[0]['code']).name,
                         self.update_data[0]['name'])

        create_worker_response = self.client.post(self.worker_url, data=self.worker_data, format='json')

        self.assertEqual(create_worker_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.worker_model.objects.count(), 2)

    def test_error_list_supervisors_workers(self):
        error_update_post = self.client.post(self.supervisor_url, self.error_data, format='json')

        self.assertEqual(error_update_post.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        error_update_post = self.client.post(self.worker_url, self.error_data, format='json')

        self.assertEqual(error_update_post.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


class AutorCommentTests(APITestCase):

    supervisor_url = ROUTES['supervisor']
    worker_url = ROUTES['workers']
    author_comment_url = ROUTES['author_comment']

    author_comment_model = models.AuthorComments
    supervisor_model = models.Supervisor
    worker_model = models.Worker

    create_supervisor_data = [{
            "code": "ТСО001951",
            "name": "Алтынбаев Артур Фаридович",
            "chat_id": None,
            "phone": "79655820336"
        }]

    create_worker_data = [{

                "code": "ТСО001099",
                "name": "Trade 10",
                "chat_id": None,
                "phone": "79677708030",
                "controller": False,
                "supervisor": "ТСО001951"
    }]

    author_comment_data = {
        'comment': "Тестовый коммент",
        'author': create_worker_data[0]['code']
    }

    def setUp(self):
        self.client = APIClient()
        self.is_authenticated = User.objects.create_user(
            username=ROUTES['auth_data']['username'],
            password=ROUTES['auth_data']['password'])
        self.response = self.client.post(ROUTES['auth'], data=ROUTES['auth_data'])
        self.token = Token.objects.get(user__username=ROUTES['auth_data']['username'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_author_comments(self):

        #  Создаю супервизора
        create_supervisor_response = self.client.post(self.supervisor_url, self.create_supervisor_data, format='json')
        self.assertEqual(create_supervisor_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.supervisor_model.objects.count(), 1)
        self.assertEqual(self.supervisor_model.objects.get().name, self.create_supervisor_data[0]['name'])

        #  Создаю торгового
        create_worker_response = self.client.post(self.worker_url, self.create_worker_data, format='json')

        self.assertEqual(create_worker_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.worker_model.objects.count(), 1)
        self.assertEqual(self.worker_model.objects.get().name, self.create_worker_data[0]['name'])

        #  Создаю комментарий
        create_author_comment_response = self.client.post(self.author_comment_url, data=self.author_comment_data,
                                                          format='json')

        self.assertEqual(create_author_comment_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.author_comment_model.objects.get().id, create_author_comment_response.data['id'])
        self.assertEqual(self.author_comment_model.objects.count(), 1)
        self.assertEqual(self.author_comment_model.objects.get().comment, self.author_comment_data['comment'])


class WorkerCommentTests(APITestCase):

    supervisor_url = ROUTES['supervisor']
    worker_url = ROUTES['workers']
    worker_comment_url = ROUTES['worker_comment']

    worker_comment_model = models.WorkerComments
    supervisor_model = models.Supervisor
    worker_model = models.Worker

    create_supervisor_data = [{
            "code": "ТСО001951",
            "name": "Алтынбаев Артур Фаридович",
            "chat_id": None,
            "phone": "79655820336"
        }]

    create_worker_data = [{

                "code": "ТСО001099",
                "name": "Trade 10",
                "chat_id": None,
                "phone": "79677708030",
                "controller": False,
                "supervisor": "ТСО001951"
    }]

    worker_comment_data = {
        'comment': "Тестовый коммент",
        'worker': create_worker_data[0]['code']
    }

    def setUp(self):
        self.client = APIClient()
        self.is_authenticated = User.objects.create_user(
            username=ROUTES['auth_data']['username'],
            password=ROUTES['auth_data']['password'])
        self.response = self.client.post(ROUTES['auth'], data=ROUTES['auth_data'])
        self.token = Token.objects.get(user__username=ROUTES['auth_data']['username'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_worker_comments(self):

        #  Создаю супервизора
        create_supervisor_response = self.client.post(self.supervisor_url, self.create_supervisor_data, format='json')
        self.assertEqual(create_supervisor_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.supervisor_model.objects.count(), 1)
        self.assertEqual(self.supervisor_model.objects.get().name, self.create_supervisor_data[0]['name'])

        #  Создаю торгового
        create_worker_response = self.client.post(self.worker_url, self.create_worker_data, format='json')
        self.assertEqual(create_worker_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.worker_model.objects.count(), 1)
        self.assertEqual(self.worker_model.objects.get().name, self.create_worker_data[0]['name'])

        #  Создаю комментарий
        create_worker_comment_response = self.client.post(self.worker_comment_url, data=self.worker_comment_data,
                                                          format='json')
        self.assertEqual(create_worker_comment_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.worker_comment_model.objects.get().id, create_worker_comment_response.data['id'])
        self.assertEqual(self.worker_comment_model.objects.count(), 1)
        self.assertEqual(self.worker_comment_model.objects.get().comment, self.worker_comment_data['comment'])
