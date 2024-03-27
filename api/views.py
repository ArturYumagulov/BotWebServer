import logging
import requests as web_requests
import environ

from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from census.models import Census
from .services import send_message_bot
from tasks import models
from . import serializers

logger = logging.getLogger(__name__)

env = environ.Env()
environ.Env.read_env('BotWebServer/.env')


class TaskViewSet(ModelViewSet):

    """
    <hr>
    <b>GET</b> - получение списка задач \n
    <b>POST</b> - создание задачи \n
    <b>PUT</b> - обновление задачи \n
    <hr>
    <b>Обозначение полей</b>\n
    <br>
    <b><em>number</em></b> - Код 1С\n
    <b><em>name</em></b> - Содержание \n
    <b><em>date</em></b> - Дата \n
    <b><em>status</em></b> - Статус \n
    <b><em>deadline</em></b> - Срок выполнения \n
    <b><em>edited</em></b> - Изменен (true-да, false-нет)\n
    <b><em>worker</em></b> - Исполнитель \n
    <b><em>partner</em></b> - Контрагент \n
    <b><em>author</em></b> - Автор \n
    <b><em>author_comment</em></b> - Комментарий автора \n
    <b><em>worker_comment</em></b> - Комментарий исполнителя \n
    <b><em>base</em></b> - Основание \n
    \n
    \n
    """

    model = models.Task
    serializer_class = serializers.TaskSerializer
    queryset = models.Task.objects.all()
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        """Вывод всех задач"""

        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        logger.info(f"{request.method} - {request.path} - {request.META['REMOTE_ADDR']} - {status.HTTP_200_OK}")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):  # noqa
        """Создание задачи"""

        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - saving data - "
                        f"{status.HTTP_201_CREATED}")
            send_message = send_message_bot(data)
            if send_message['result']:
                logger.info(f"Сообщение {data} отправлено - {send_message['description']}")
            else:
                logger.error(f"Сообщение {data} не отправлено - {send_message['description']}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - не сохранено - "
                     f"serializer_error:{serializer.errors} {status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
        return Response(serializer.errors, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def put(self, request):  # noqa
        """Изменение существующей задачи"""

        data = request.data

        try:
            serializer = self.serializer_class(data=data, instance=self.queryset.get(number=data['number']))
            logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - data_have - "
                        f"{status.HTTP_200_OK}")
            if serializer.is_valid():
                serializer.save()
                logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - saving data - "
                            f"{status.HTTP_201_CREATED}")

                if serializer.data['status'] == "Новая":
                    if send_message_bot(data):
                        logger.info(f"Сообщение {data} отправлено")
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        logger.error(f"Сообщение {data} не отправлено")
                elif serializer.data['status'] == "Выполнено" or serializer.data['status'] == "Переадресована":
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                elif serializer.data['status'] == "ОтклоненоСистемой":
                    task = self.queryset.get(number=data['number'])
                    chat_id = task.worker.chat_id
                    message_id = task.message_id
                    message_del_url = f'https://api.telegram.org/bot{env.str("BOT_TOKEN")}/deleteMessage?' \
                                      f'chat_id={chat_id}&message_id={message_id}'

                    r = web_requests.get(message_del_url)

                    if r.json()['ok']:
                        task.message_id = "Удалено"
                        task.save()
                        logger.info(f"Сообщение {task.number} из чата {task.worker.name} удалено")
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        logger.error(f"Сообщение {task.number} из чата {task.worker.name} не удалено - {r.json()['description']}")
                        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

            logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - не сохранено - "
                         f"serializer_error:{serializer.errors} - {status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
            return Response(serializer.errors, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        except self.model.DoesNotExist:
            logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                         f"serializer_error:{'Данная задача не существует'} - {status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
            return Response({'detail': 'Данная задача не существует'}, status=status.HTTP_404_NOT_FOUND)


class BaseViewSet(ModelViewSet):
    """
    Выгрузка и загрузка оснований
    <hr>
    <b>GET</b> - получение\n
    <b>POST</b> - создание\n
    <b>PUT</b> - обновление\n
    <hr>
    <b><em>number</em></b> - Код 1С\n
    <b><em>name</em></b> - Название \n
    <b><em>date</em></b> - Дата \n
    """

    model = models.Basics
    serializer_class = serializers.BasicSerializer
    queryset = models.Basics.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        logger.info(f"{request.method} - {request.path} - {request.META['REMOTE_ADDR']} - {status.HTTP_200_OK}")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request): # noqa

        data = request.data
        if isinstance(data, list):

            serializer = self.serializer_class(data=data, many=True)

            if serializer.is_valid():
                serializer.save()
                logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                            f"saving data - {status.HTTP_201_CREATED}")
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                             f"не сохранено - serializer_error:{serializer.errors} "
                             f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
                return Response(data=serializer.errors, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        else:
            logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                         "{'detail': 'ожидался массив данных'} - "
                         f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
            return Response({'detail': 'ожидался массив данных'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def put(self, request, *args, **kwargs):

        data = request.data

        if isinstance(data, list):

            for i in data:

                serializer = self.serializer_class(data=i, instance=self.queryset.get(number=i['number']), many=False)

                if serializer.is_valid():
                    serializer.save()
                    logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                                f"- saving data - {status.HTTP_201_CREATED}")
                else:
                    logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                                 f"- не сохранено - serializer_error:{serializer.errors} "
                                 f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
                    return Response(serializer.errors, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        else:
            logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                         "{'detail': 'ожидался массив данных'} - "
                         f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
            return Response({'detail': 'ожидался массив данных'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        return Response({'detail': f"Данные - обновлены"}, status=status.HTTP_201_CREATED)


class PartnersViewSet(ModelViewSet):
    """
    Выгрузка и загрузка контрагентов - множественная

    <hr>
    <b>GET</b> - получение\n
    <b>POST</b> - создание\n
    <b>PUT</b> - обновление\n
    <hr>
    <b><em>code</em></b> - Код 1С\n
    <b><em>name</em></b> - Имя \n
    """

    serializer_class = serializers.PartnerSerializer
    queryset = models.Partner.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        logger.info(f"{request.method} - {request.path} - {request.META['REMOTE_ADDR']} - {status.HTTP_200_OK}")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request): # noqa

        data = request.data

        if isinstance(data, list):
            serializer = self.serializer_class(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                         "{'detail': 'ожидался массив данных'} - "
                         f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
            return Response({'detail': 'ожидался массив данных'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def put(self, request, *args, **kwargs):

        data = request.data

        if isinstance(data, list):

            for i in data:
                serializer = self.serializer_class(data=i,
                                                   instance=self.queryset.get(code=i['code']), many=False)

                if serializer.is_valid():
                    serializer.save()
                    logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                                f"- saving data - {status.HTTP_201_CREATED}")
        else:
            logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                         "{'detail': 'ожидался массив данных'} - "
                         f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
            return Response({'detail': 'ожидался массив данных'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        return Response({'result': True, 'detail': f"data updated"}, status=status.HTTP_201_CREATED)


class PartnersWorkerViewSet(ModelViewSet):

    model = models.PartnerWorker
    serializer_class = serializers.PartnerWorkerSerializer
    queryset = models.PartnerWorker.objects.all()

    def list(self, request):  # noqa
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        logger.info(f"{request.method} - {request.path} - {request.META['REMOTE_ADDR']} - {status.HTTP_200_OK}")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request): # noqa

        data = request.data

        serializer = self.serializer_class(data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                        f"- saving data - {status.HTTP_201_CREATED}")
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                     f"{serializer.errors} - "
                     f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
        return Response({'detail': 'ожидался массив данных'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


class WorkerViewSet(ModelViewSet):

    serializer_class = serializers.WorkerSerializer
    queryset = models.Worker.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        logger.info(f"{request.method} - {request.path} - {request.META['REMOTE_ADDR']} - {status.HTTP_200_OK}")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request): # noqa

        data = request.data

        if isinstance(data, list):
            serializer = self.serializer_class(data=data, many=True)

            if serializer.is_valid():
                serializer.save()
                logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                            f"- saving data - {status.HTTP_201_CREATED}")
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        else:
            logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                         "{'detail': 'ожидался массив данных'} - "
                         f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
            return Response({'detail': 'ожидался массив данных'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def put(self, request, *args, **kwargs):

        data = request.data

        if isinstance(data, list):
            for i in data:
                serializer = self.serializer_class(many=False,
                                                   instance=self.queryset.get(code=i['code']), data=i)
                if serializer.is_valid():
                    serializer.save()
                    logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                                f"- saving data - {status.HTTP_201_CREATED}")
                else:
                    logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                                 f"- saving data - {status.HTTP_201_CREATED}")
                    return Response(serializer.errors, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

            return Response({'detail': 'Данные успешно обновлены'}, status=status.HTTP_201_CREATED)
        logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                     "{'detail': 'ожидался массив данных'} - "
                     f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
        return Response({'detail': 'ожидался массив данных'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


class SupervisorViewSet(ModelViewSet):

    serializer_class = serializers.SupervisorSerializer
    queryset = models.Supervisor.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        logger.info(f"{request.method} - {request.path} - {request.META['REMOTE_ADDR']} - {status.HTTP_200_OK}")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request): # noqa

        data = request.data

        if isinstance(data, list):

            serializer = self.serializer_class(data=data, many=True)

            if serializer.is_valid():
                serializer.save()
                logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                            f"- saving data - {status.HTTP_201_CREATED}")
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                         "{'detail': 'ожидался массив данных'} - "
                         f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
            return Response({'detail': 'ожидался массив данных'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def put(self, request, *args, **kwargs):

        data = request.data

        if isinstance(data, list):
            for i in data:
                serializer = self.serializer_class(many=False,
                                                   instance=self.queryset.get(code=i['code']), data=i)
                if serializer.is_valid():
                    serializer.save()
                    logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                                f"- saving data - {status.HTTP_201_CREATED}")
                else:
                    return Response(serializer.errors, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
            return Response({'detail': 'Данные успешно обновлены'}, status=status.HTTP_201_CREATED)
        logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                     "{'detail': 'ожидался массив данных'} - "
                     f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
        return Response({'detail': 'ожидался массив данных'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


class AuthorCommentsViews(ModelViewSet):

    serializer_class = serializers.AuthorCommentsSerializer
    queryset = models.AuthorComments.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        logger.info(f"{request.method} - {request.path} - {request.META['REMOTE_ADDR']} - {status.HTTP_200_OK}")
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request): # noqa

        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                        f"- saving data - {status.HTTP_201_CREATED}")
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                     f"{serializer.errors} - "
                     f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
        return Response(data=serializer.errors, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


class WorkerCommentsViews(ModelViewSet):

    serializer_class = serializers.WorkerCommentsSerializer
    queryset = models.WorkerComments.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        logger.info(f"{request.method} - {request.path} - {request.META['REMOTE_ADDR']} - {status.HTTP_200_OK}")
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request): # noqa

        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                        f"- saving data - {status.HTTP_201_CREATED}")
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                     f"{serializer.errors} - "
                     f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
        return Response(data=serializer.errors, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


class TaskViewListSet(ModelViewSet):

    serializer_class = serializers.TaskListSerializer
    queryset = models.Task.objects.all()

    def list(self, request, *args, **kwargs):
        """Вывод всех задач"""

        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        logger.info(f"{request.method} - {request.path} - {request.META['REMOTE_ADDR']} - {status.HTTP_200_OK}")
        return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class AllTaskViewListSet(ModelViewSet):
#
#     serializer_class = serializers.TaskListSerializer
#     queryset = models.Task.objects.all()
#
#     def list(self, request, *args, **kwargs):
#         """Вывод всех услуг"""
#
#         queryset = self.queryset.all()
#         serializer = self.serializer_class(queryset, many=True)
#         logger.info(f"{request.method} - {request.path} - {request.META['REMOTE_ADDR']} - {status.HTTP_200_OK}")
#         return Response(serializer.data, status=status.HTTP_200_OK)


class ResultListView(ModelViewSet):

    serializer_class = serializers.ResultSerializer
    queryset = models.Result.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        logger.info(f"{request.method} - {request.path} - {request.META['REMOTE_ADDR']} - {status.HTTP_200_OK}")
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request): # noqa

        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                        f"- saving data - {status.HTTP_201_CREATED}")
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                     f"{serializer.errors} - "
                     f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        data = request.data
        serializer = self.serializer_class(data=data,
                                           instance=models.WorkerComments.objects.get(pk=data.pk))

        if serializer.is_valid():
            serializer.save()
            logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                        f"- saving data - {status.HTTP_201_CREATED}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                     f"{serializer.errors} - "
                     f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResultGroupListView(ModelViewSet):

    serializer_class = serializers.ResultGroupSerializer
    queryset = models.ResultGroup.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        logger.info(f"{request.method} - {request.path} - {request.META['REMOTE_ADDR']} - {status.HTTP_200_OK}")
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request): # noqa

        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                        f"- saving data - {status.HTTP_201_CREATED}")
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                     f"{serializer.errors} - "
                     f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        data = request.data
        serializer = self.serializer_class(data=data,
                                           instance=self.queryset.get(code=data['code']))

        if serializer.is_valid():
            serializer.save()
            logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                        f"- saving data - {status.HTTP_201_CREATED}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                     f"{serializer.errors} - "
                     f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResultDataListView(ModelViewSet):

    serializer_class = serializers.ResultDataSerializer
    queryset = models.ResultData.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        logger.info(f"{request.method} - {request.path} - {request.META['REMOTE_ADDR']} - {status.HTTP_200_OK}")
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request): # noqa

        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                        f"- saving data - {status.HTTP_201_CREATED}")
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                     f"{serializer.errors} - "
                     f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        data = request.data
        serializer = self.serializer_class(data=data,
                                           instance=self.queryset.get(pk=data.pk))

        if serializer.is_valid():
            serializer.save()
            logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                        f"- saving data - {status.HTTP_201_CREATED}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                     f"{serializer.errors} - "
                     f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllTasksUpdateView(ModelViewSet):
    """Вывод только измененных задач"""
    queryset = models.Task.objects.filter(edited=True).exclude(status="Загружено")
    serializer_class = serializers.AllTaskListSerializer

    def create(self, request):  # noqa

        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                        f"- saving data - {status.HTTP_201_CREATED}")
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                     f"{serializer.errors} - "
                     f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        data = request.data
        serializer = self.serializer_class(data=data,
                                           instance=self.queryset.get(number=data['number']))

        if serializer.is_valid():
            serializer.save()
            logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} "
                        f"- saving data - {status.HTTP_201_CREATED}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - "
                     f"{serializer.errors} - "
                     f"{status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# FILTERS

class WorkerForwardViewSet(ModelViewSet):
    """
    Фильтр сотрудников при переадресовывании задачи
    исключается number запросившего и chat_id=null
    """

    serializer_class = serializers.WorkerSerializer
    queryset = models.Worker.objects.all()

    def list(self, request, code):  # noqa
        queryset = self.queryset.filter(chat_id__isnull=False).exclude(code=code)
        serializer = self.serializer_class(queryset, many=True)
        logger.info(f"{request.method} - {request.path} - {request.META['REMOTE_ADDR']} - {status.HTTP_200_OK}")
        return Response(serializer.data, status=status.HTTP_200_OK)


class TasksFilterViews(generics.ListAPIView):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['worker', 'edited', 'status']


class WorkerFilterViews(generics.ListAPIView):
    queryset = models.Worker.objects.all()
    serializer_class = serializers.WorkerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['chat_id', 'phone', 'controller', 'code']


class PartnerWorkerFilterViews(generics.ListAPIView):
    queryset = models.PartnerWorker.objects.all()
    serializer_class = serializers.PartnerWorkerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['partner', 'id', 'code']


class ResultDataFilterViews(generics.ListAPIView):

    serializer_class = serializers.ResultDataSerializer

    def get_queryset(self):
        queryset = models.ResultData.objects.all()
        group_code = self.request.query_params.get('group')
        group = get_object_or_404(models.ResultGroup, code=group_code)
        if group is not None:
            queryset = queryset.filter(group=group)
        return queryset


class CensusView(ModelViewSet):

    serializer_class = serializers.CensusSerializer
    queryset = Census.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        logger.info(f"{request.method} - {request.path} - {request.META['REMOTE_ADDR']} - {status.HTTP_200_OK}")
        return Response(serializer.data, status=status.HTTP_200_OK)


class CensusFilterViews(generics.ListAPIView):
    queryset = Census.objects.all()
    serializer_class = serializers.CensusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task']


class CensusUpdate(ModelViewSet):
    serializer_class = serializers.CensusUpdateSerializer
    queryset = Census.objects.all()

    def put(self, request):  # noqa
        """Изменение существующей задачи"""

        data = request.data

        serializer = self.serializer_class(data=data, instance=self.queryset.get(pk=data['pk']))
        logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - data_have - "
                    f"{status.HTTP_200_OK}")
        if serializer.is_valid():
            serializer.save()
            logger.info(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - saving data - "
                        f"{status.HTTP_201_CREATED}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"{request.method} - {request.path} - {data} - {request.META['REMOTE_ADDR']} - не сохранено - "
                     f"serializer_error:{serializer.errors} - {status.HTTP_415_UNSUPPORTED_MEDIA_TYPE}")
        return Response(serializer.errors, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


class TaskMessageUpdateView(ModelViewSet):

    serializer_class = serializers.TaskMessageUpdateSerializer
    queryset = models.Task.objects.all()

    def put(self, request, *args, **kwargs):

        data = request.data

        serializer = self.serializer_class(data=data, instance=self.queryset.get(number=data['number']))
        if serializer.is_valid():
            serializer.save()
        logger.info(f"{request.method} - {request.path} - {request.META['REMOTE_ADDR']} - {status.HTTP_200_OK}")
        return Response(serializer.data, status=status.HTTP_200_OK)
