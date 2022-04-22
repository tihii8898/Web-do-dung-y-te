from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import products
# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/products/',
        '/api/products/create',
        '/api/products/update',
        '/api/products/delete',
        '/api/products/<int:id>',
        
    ]
    return Response(routes)


@api_view(['GET'])
def getProducts(request):
    return Response(products)