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
    'result_group': '/api/v1/result-group/',
    'auth': '/api/v1/token-auth/',
    'auth_data': {'username': "test_user", 'password': "test12345"}
}


class DataTestClass(APITestCase):
    base_url = ROUTES['base']
    group_url = ROUTES['result_group']

    partners_url = ROUTES['partners']
    partner_worker_url = ROUTES['partner_worker']

    supervisor_url = ROUTES['supervisor']
    worker_url = ROUTES['workers']
    author_comment_url = ROUTES['author_comment']

    base_model = models.Basics
    partner_model = models.Partner
    partner_worker_model = models.PartnerWorker
    supervisor_model = models.Supervisor
    worker_model = models.Worker

    group_data = {
        "code": "000000002",
        "name": "Pазработка Контрагента"
    }

    base_create_data = [
        {
            "number": "00000142871",
            "name": "Событие 00000142871 от 05.06.2023 16:37:47",
            "date": "2023-06-05T16:37:47Z",
            "group": "000000002"
        },
        {
            "number": "00000142866",
            "name": "Событие 00000142866 от 02.06.2023 16:59:07",
            "date": "2023-06-02T16:59:07Z",
            "group": "000000002"
        },
        {
            "number": "00000142865",
            "name": "Событие 00000142865 от 02.06.2023 15:34:20",
            "date": "2023-06-02T15:34:20Z",
            "group": "000000002"
        }
    ]

    base_update_data = [
        {
            "number": "00000142871",
            "name": "Изменено",
            "date": "2023-06-05T16:37:47Z",
            "group": "000000002"
        }
    ]
    base_error_data = {
            "number": "00000142871",
            "name": "Изменено",
            "date": "2023-06-05T16:37:47Z",
            "group": "000000002"
        }

    partners_create_data = [
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

    partners_update_data = [
        {
            "code": "ТСО007316",
            "name": "Изменено"
        }
    ]
    partners_error_data = {
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
            "name": "Сотрудник 2",
            "positions": "Директор",
            "code": "F00001716",
            "partner": "ТСО017919"
        }

    ]

    supervisor_create_data = [
        {
            "code": "ТСО001951",
            "name": "Алтынбаев Артур Фаридович",
            "chat_id": None,
            "phone": "79655820336",
            'head': None,
        },
        {
            "code": "ТСО000780",
            "name": "Габитов Ильнар Салимуллович",
            "chat_id": None,
            "phone": "79600847615",
            'head': None,
        },
        {
            "code": "ТСО012297",
            "name": "Галеев Рамиль Мухаметшакирович",
            "chat_id": None,
            "phone": "79173908880",
            'head': None,
        }
    ]

    supervisor_update_data = [
        {
            "code": "ТСО000780",
            "name": "Изменено",
            "chat_id": None,
            "phone": "79600847615"
        }
    ]
    supervisor_error_data = {
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
    author_comment_data = {
        'comment': "Тестовый коммент",
        'author': worker_data[0]['code']
    }

    worker_comment_data = {
        'comment': "Тестовый коммент",
        'worker': worker_data[0]['code']
    }

    def setUp(self):
        self.client = APIClient()
        self.is_authenticated = User.objects.create_user(
            username=ROUTES['auth_data']['username'],
            password=ROUTES['auth_data']['password'])
        self.response = self.client.post(ROUTES['auth'], data=ROUTES['auth_data'])
        self.token = Token.objects.get(user__username=ROUTES['auth_data']['username'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


class BaseTests(DataTestClass, APITestCase):
    """Тестирование оснований"""

    def test_create_and_update_basic(self):
        create_group = self.client.post(self.group_url, self.group_data)
        self.assertEqual(create_group.status_code, status.HTTP_201_CREATED)
        create_response = self.client.post(self.base_url, self.base_create_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.base_model.objects.count(), 3)
        update_response = self.client.put(self.base_url, self.base_update_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.base_model.objects.get(number=self.base_update_data[0]['number']).name,
                         self.base_update_data[0]['name'])

    def test_error_list_data(self):
        error_update_post = self.client.post(self.base_url, self.base_error_data, format='json')
        self.assertEqual(error_update_post.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


class PartnersTests(DataTestClass):

    def test_create_and_update_partners(self):
        create_response = self.client.post(self.partners_url, self.partners_create_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.partner_model.objects.count(), 3)
        update_response = self.client.put(self.partners_url, self.partners_update_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.partner_model.objects.get(code=self.partners_update_data[0]['code']).name,
                         self.partners_update_data[0]['name'])
        create_worker_response = self.client.post(self.partner_worker_url, data=self.partner_worker_data, format='json')
        self.assertEqual(create_worker_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.partner_worker_model.objects.count(), 2)

    def test_error_list_partners(self):
        error_update_post = self.client.post(self.partners_url, self.partners_error_data, format='json')
        self.assertEqual(error_update_post.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        error_update_post = self.client.post(self.partner_worker_url, self.partners_error_data, format='json')
        self.assertEqual(error_update_post.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
