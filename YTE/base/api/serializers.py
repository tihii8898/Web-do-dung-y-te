from dataclasses import field
from rest_framework.serializers import ModelSerializer
from base.models import *


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrdersSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ShippingAddressSeralizer(ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'
