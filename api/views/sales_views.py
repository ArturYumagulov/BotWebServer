import logging

from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response

from api.serializers import sales as serializers
from sales.models import Product, Order, OrderItem, RetailUnit

logger = logging.getLogger(__name__)


class ProductsView(ModelViewSet):
    """Список номенклатуры"""
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()

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


class OrdersView(ModelViewSet):
    """Реализация"""
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.all()

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


class OrderItemView(ModelViewSet):
    """Поля в реализации"""
    serializer_class = serializers.OrderItemSerializer
    queryset = OrderItem.objects.all()

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


class RetailUnitView(ModelViewSet):
    """Список торговых точек"""
    serializer_class = serializers.RetailUnitSerializer
    queryset = RetailUnit.objects.all()

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

