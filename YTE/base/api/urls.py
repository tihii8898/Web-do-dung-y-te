from django.urls import path
from . import views


urlpatterns = [
    path('',views.getRoutes),
    path('products',views.getProducts),
    path('orders',views.getOrders),
    path('order-items',views.getOrderItem),
    path('thanh-toan',views.getShippingAddress)
]
