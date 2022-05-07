from atexit import register
from email import message
from functools import reduce
from math import prod
from unicodedata import category
from django.db.models import Q
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import *

from django import template
register = template.Library()

@register.filter
def mul(value,arg):
    '''
    hàm nhân dùng cho cart subtotal
    '''
    try: 
        value = int(value)
        arg = int(arg)
        if arg: 
            return value * arg
    except:
        pass
    return ''
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
    if request.user.is_authenticated:
        return redirect('home')

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
            return redirect('home')
        else:
            messages.error(
                request, 'Tên đăng nhập hoặc mật khẩu không hợp lệ ! ! !')

    context = {
        'page': page,
    }
    return render(
        request,
        'base/login-signup.html',
        context
    )


def signupPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(
                request, 'Có lỗi xảy ra trong quá trình đăng kí, xin hãy thử lại T.T ')

    context = {
        'form': form

    }
    return render(
        request,
        'base/login-signup.html',
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
    relate_products = Product.objects.all().filter(query)
    order, created = Order.objects.get_or_create(user=request.user)
    if request.method == 'POST':
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
