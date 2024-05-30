import logging

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from api.serializers import census as serializers
from census.models import Census, AddressesCount

logger = logging.getLogger(__name__)


class CensusUpdate(ModelViewSet):
    serializer_class = serializers.CensusUpdateSerializer
    queryset = Census.objects.all()

    def put(self, request):  # noqa
        """Изменение существующей задачи"""

        data = request.data

        serializer = self.serializer_class(data=data, instance=self.queryset.get(pk=data['census_id']))
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
    filterset_fields = ['task', 'address_id', 'loaded']


class AddressesCountView(ModelViewSet):

    serializer_class = serializers.AddressesCountSerializer
    queryset = AddressesCount.objects.all()

    def put(self, request):

        data = request.data

        serializer = self.serializer_class(data=data, instance=self.queryset.get(pk=data['census_id']))
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
