import logging
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
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

    serializer_class = TaskSerializer
    basic_serializer = BasicSerializer
    queryset = Task.objects.all()

    def list(self, request, *args, **kwargs):
        """Вывод всех услуг"""

        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        logger.info("Get response")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):  # noqa
        """Создание поста"""

        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            send_message_bot(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):  # noqa
        """Изменение существующего поста"""

        data = request.data
        try:
            serializer = self.serializer_class(data=data, instance=Task.objects.get(number=data['number']))

            if serializer.is_valid():
                serializer.save()
                send_message_bot(data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({'detail': 'Данная задача не существует'}, status=status.HTTP_400_BAD_REQUEST)


class ResultDataFilterViews(generics.ListAPIView):

    serializer_class = ResultDataSerializer

    def get_queryset(self):
        queryset = ResultData.objects.all()
        group_name = self.request.query_params.get('group')
        group = get_object_or_404(ResultGroup, pk=group_name)
        if group_name is not None:
            queryset = queryset.filter(group=group)
        return queryset


class BaseViewSet(ModelViewSet):
    """
    Основание
    <hr>
    <b>GET</b> - получение списка задач \n
    <b>POST</b> - создание задачи \n
    <b>PUT</b> - обновление задачи \n
    <hr>
    <b><em>number</em></b> - Код 1С\n
    <b><em>name</em></b> - Название \n
    <b><em>date</em></b> - Дата \n
    """

    serializer_class = BasicSerializer
    queryset = Basics.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request): # noqa

        data = request.data

        serializer = self.serializer_class(data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        data = request.data
        serializer = self.serializer_class(data=data,
                                           instance=Basics.objects.get(number=data['number']), many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartnersViewSet(ModelViewSet):
    """
    Контрагент

    <hr>
    <b>GET</b> - получение списка задач \n
    <b>POST</b> - создание задачи \n
    <b>PUT</b> - обновление задачи \n
    <hr>
    <b><em>code</em></b> - Код 1С\n
    <b><em>name</em></b> - Имя \n
    """

    serializer_class = PartnerSerializer
    queryset = Partner.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request): # noqa

        data = request.data

        serializer = self.serializer_class(data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        data = request.data
        serializer = self.serializer_class(data=data,
                                           instance=Basics.objects.get(number=data['number']))

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartnersWorkerViewSet(ModelViewSet):

    serializer_class = PartnerWorkerSerializer
    queryset = PartnerWorker.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request): # noqa

        data = request.data

        serializer = self.serializer_class(data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        data = request.data
        serializer = self.serializer_class(data=data,
                                           instance=PartnerWorker.objects.get(partner=data['partner']), many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkerViewSet(ModelViewSet):

    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request): # noqa

        data = request.data

        serializer = self.serializer_class(data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        data = request.data

        if len(data) > 0:
            for i in data:
                serializer = self.serializer_class(many=False,
                                                   instance=self.queryset.get(code=i['code']), data=i)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail': 'Данные успешно обновлены'}, status=status.HTTP_201_CREATED)
        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)


class SupervisorViewSet(ModelViewSet):

    serializer_class = SupervisorSerializer
    queryset = Supervisor.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request): # noqa
        data = request.data

        serializer = self.serializer_class(data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        data = request.data
        if data > 0:
            for i in data:
                serializer = self.serializer_class(many=False,
                                                   instance=self.queryset.get(code=i['code']), data=i)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail': 'Данные успешно обновлены'}, status=status.HTTP_201_CREATED)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class AuthorCommentsViews(ModelViewSet):

    serializer_class = AuthorCommentsSerializer
    queryset = AuthorComments.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request): # noqa

        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        data = request.data
        serializer = self.serializer_class(data=data,
                                           instance=Basics.objects.get(number=data['number']))

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkerCommentsViews(ModelViewSet):

    serializer_class = WorkerCommentsSerializer
    queryset = WorkerComments.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request): # noqa

        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        data = request.data
        serializer = self.serializer_class(data=data,
                                           instance=WorkerComments.objects.get(pk=data.pk))

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkerForwardViewSet(ModelViewSet):
    """Фильтр сотрудников при переадресовывании задачи
        исключается number запросивщего и chat_id=null
    """

    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()

    def list(self, request, code):  # noqa
        queryset = self.queryset.filter(chat_id__isnull=False).exclude(code=code)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskViewListSet(ModelViewSet):

    serializer_class = TaskListSerializer
    queryset = Task.objects.all()

    def list(self, request, *args, **kwargs):
        """Вывод всех услуг"""

        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ResultListView(ModelViewSet):

    serializer_class = ResultSerializer
    queryset = Result.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request): # noqa

        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        data = request.data
        serializer = self.serializer_class(data=data,
                                           instance=WorkerComments.objects.get(pk=data.pk))

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResultGroupListView(ModelViewSet):

    serializer_class = ResultGroupSerializer
    queryset = ResultGroup.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request): # noqa

        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        data = request.data
        serializer = self.serializer_class(data=data,
                                           instance=self.queryset.get(pk=data.pk))

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResultDataListView(ModelViewSet):

    serializer_class = ResultDataSerializer
    queryset = ResultData.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request): # noqa

        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        data = request.data
        serializer = self.serializer_class(data=data,
                                           instance=self.queryset.get(pk=data.pk))

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# FILTERS

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
    filterset_fields = ['partner', 'id']


class AllTasksFilterView(ModelViewSet):
    """Вывод только измененных задач"""
    queryset = Task.objects.filter(edited=True).exclude(status="Загружено")
    serializer_class = AllTaskListSerializer
    # filter_backends = [DjangoFilterBackend]

    def create(self, request):  # noqa

        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        data = request.data
        serializer = self.serializer_class(data=data,
                                           instance=self.queryset.get(pk=data.pk))

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#  TODO Добавить кеширование
#  TODO Добаввить логгирование
