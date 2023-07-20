import logging
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from urllib.parse import quote, urlencode, unquote
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import status
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .services import send_message_bot
from tasks.models import Task, Basics, Partner, Worker, AuthorComments, WorkerComments, PartnerWorker, Result, \
    ResultGroup, ResultData, Supervisor  # noqa
from .serializers import TaskSerializer, BasicSerializer, PartnerSerializer, WorkerSerializer, \
    AuthorCommentsSerializer, WorkerCommentsSerializer, TaskListSerializer, PartnerWorkerSerializer, ResultSerializer, \
    ResultGroupSerializer, ResultDataSerializer, SupervisorSerializer, AllTaskListSerializer

logger = logging.getLogger(__name__)


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

    model = Task
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

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
            if send_message_bot(data):
                logger.info(f"Сообщение {data} отправлено")
            else:
                logger.error(f"Сообщение {data} не отправлено")
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
                if send_message_bot(data):
                    logger.info(f"Сообщение {data} отправлено")
                else:
                    logger.error(f"Сообщение {data} не отправлено")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
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

    model = Basics
    serializer_class = BasicSerializer
    queryset = Basics.objects.all()

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

    serializer_class = PartnerSerializer
    queryset = Partner.objects.all()

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

        return Response({'detail': f"Данные - обновлены"}, status=status.HTTP_201_CREATED)


class PartnersWorkerViewSet(ModelViewSet):

    model = PartnerWorker
    serializer_class = PartnerWorkerSerializer
    queryset = PartnerWorker.objects.all()

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

    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()

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


class WorkerDetailView(APIView):

    def get(self, request, code: str):
        url_encode = urlencode({'url_encode': code})
        unquote_code = unquote(code)
        print(url_encode, unquote_code)
        data = {'url_encode': url_encode, 'unquote_code': unquote_code}
        worker = Worker.objects.filter(code=unquote_code)
        return Response(worker)


class SupervisorViewSet(ModelViewSet):

    serializer_class = SupervisorSerializer
    queryset = Supervisor.objects.all()

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

    serializer_class = AuthorCommentsSerializer
    queryset = AuthorComments.objects.all()

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

    serializer_class = WorkerCommentsSerializer
    queryset = WorkerComments.objects.all()

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

    serializer_class = TaskListSerializer
    queryset = Task.objects.all()

    def list(self, request, *args, **kwargs):
        """Вывод всех услуг"""

        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        logger.info(f"{request.method} - {request.path} - {request.META['REMOTE_ADDR']} - {status.HTTP_200_OK}")
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResultListView(ModelViewSet):

    serializer_class = ResultSerializer
    queryset = Result.objects.all()

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
                                           instance=WorkerComments.objects.get(pk=data.pk))

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

    serializer_class = ResultGroupSerializer
    queryset = ResultGroup.objects.all()

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

    serializer_class = ResultDataSerializer
    queryset = ResultData.objects.all()

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
    queryset = Task.objects.filter(edited=True).exclude(status="Загружено")
    serializer_class = AllTaskListSerializer

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

    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()

    def list(self, request, code):  # noqa
        queryset = self.queryset.filter(chat_id__isnull=False).exclude(code=code)
        serializer = self.serializer_class(queryset, many=True)
        logger.info(f"{request.method} - {request.path} - {request.META['REMOTE_ADDR']} - {status.HTTP_200_OK}")
        return Response(serializer.data, status=status.HTTP_200_OK)


class TasksFilterViews(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['worker', 'edited', 'status']


class WorkerFilterViews(generics.ListAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['chat_id', 'phone', 'controller', 'code']


class PartnerWorkerFilterViews(generics.ListAPIView):
    queryset = PartnerWorker.objects.all()
    serializer_class = PartnerWorkerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['partner', 'id', 'code']


class ResultDataFilterViews(generics.ListAPIView):

    serializer_class = ResultDataSerializer

    def get_queryset(self):
        queryset = ResultData.objects.all()
        group_code = self.request.query_params.get('group')
        group = get_object_or_404(ResultGroup, code=group_code)
        if group is not None:
            queryset = queryset.filter(group=group)
        return queryset


