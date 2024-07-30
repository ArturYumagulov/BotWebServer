from rest_framework import serializers

from sales import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = "__all__"


class RetailUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RetailUnit
        fields = "__all__"
