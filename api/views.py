from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .services import send_message_bot
from tasks.models import Task, Basics, Partner, Worker, AuthorComments, WorkerComments  # noqa
from .serializers import TaskSerializer, BasicSerializer, PartnerSerializer, WorkerSerializer, \
    AuthorCommentsSerializer, WorkerCommentsSerializer


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


class TasksFilterViews(generics.ListAPIView):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['worker', 'edited', 'status']


class WorkerFilterViews(generics.ListAPIView):

    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['chat_id', 'phone']


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
        serializer = self.serializer_class(data=data,
                                           instance=Worker.objects.get(code=data['code']))

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
