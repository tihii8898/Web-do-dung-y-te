from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import *
from .serializers import *


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/products',
        'GET /api/product/:id',
        'GET /api/order',
        'GET /api/thanh-toan',
    ]
    
    return Response(routes)


@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    products_serializer = ProductSerializer(products,many=True)
    
    return Response(products_serializer.data)

@api_view(['GET'])
def getOrders(request):
    orders = Order.objects.all()
    orders_serializer = OrdersSerializer(orders,many = True)
    
    return Response(orders_serializer.data)


@api_view(['GET'])
def getOrderItem(request):
    orders_item = OrderItem.objects.all()
    orders_item_serializer = OrderItemSerializer(orders_item,many = True)
    
    return Response(orders_item_serializer.data)

@api_view(['GET'])
def getShippingAddress(request):
    ship_address = ShippingAddress.objects.all()
    ship_address_serializer = ShippingAddressSeralizer(ship_address,many=True)
    return Response(ship_address_serializer.data)