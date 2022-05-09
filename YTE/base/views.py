from atexit import register
from email import message
from functools import reduce
from math import prod
from unicodedata import category
from wsgiref.util import request_uri
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import re_path
from .models import *


# Create your views here.


def homePage(request):
    products = Product.objects.all()[:5]
    products_latest = Product.objects.all().order_by('createAt').reverse()[:5]
    context = {
        'products': products,
        'products_latest': products_latest
    }

    return render(
        request,
        'base/index.html',
        context
    )


@login_required(login_url='/login')
def cart(request):
    user = request.user
    order = Order.objects.get(user= user)
    orderItem_set = order.orderitem_set.all()
    
    if order.orderitem_set.all().count() ==0:
        subTotal=0
    elif order.orderitem_set.all().count() <2:
        subTotal = orderItem_set[0].price * orderItem_set[0].count
    else:
        subTotal = reduce(lambda x,y: x.price * x.count + y.price*y.count , orderItem_set)
    print('Item Count: {}'.format(order.orderitem_set.all().count()))
    
    
    context = {
        'orderItem_set' : orderItem_set,
        'subTotal': subTotal,
    }

    if request.method == 'POST':
        id = request.POST.get('id')
        print('ID: ',id)
        print('asdasd')
        delete_orderItem = OrderItem.objects.get(id = id)
        delete_orderItem.delete()
        return redirect('cart')
    
    return render(
        request,
        'base/cart.html',
        context
    )


def loginPage(request):
    page = 'login'
    next= request.GET.get('next','/')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, 'Tài khoảng không tồn tại ! ! !')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect(next)
        else:
            messages.error(
                request, 'Tên đăng nhập hoặc mật khẩu không hợp lệ ! ! !')

    context = {
        'nextFromLG':next,
        'page': page,
    }
    return render(
        request,
        'base/account.html',
        context
    )


def signupPage(request):
    next= request.GET.get('next','/')
    print('#########',next)
    if request.method == 'POST':
        username= request.POST['username']
        password1= request.POST['password1']
        password2= request.POST['password2']
        email= request.POST['email']
        # else:
        try:
            user = User.objects.create_user(username,email,password1)
            user.username= user.username.lower()
            user.save()
            login(request,user)
            return redirect(next)
        except:
            messages.error(
                request, 'Có lỗi xảy ra trong quá trình đăng kí, xin hãy thử lại T.T ')
    context = {
        

    }
    return render(
        request,
        'base/account.html',
        context



    )


def logoutUser(request):
    logout(request)
    return redirect('home')


def productsPage(request):

    context = {}
    return render(
        request,
        'base/products.html',
        context
    )


def productInfo(request, pk):
    product = Product.objects.get(id=pk) 
    query = Q(category = product.category)
    relate_products = Product.objects.all().filter(query)[:5]
    if request.method == 'POST':
        # next = request.POST.get('next')
        # print('------ PRE: {} ------'.format(next))
        # if not request.user.is_authenticated:
        #     return redirect('login')
        order, created = Order.objects.get_or_create(user=request.user)
        OrderItem.objects.create(
            product=product,
            order=order,
            price= product.price,
            name=product.name,
            image= product.image,
            count = request.POST.get('count-product')
        )
        return redirect('cart')

    context = {
        'product': product,
        'relate_products':relate_products
    }
    return render(
        request,
        'base/product-details.html',
        context
    )
