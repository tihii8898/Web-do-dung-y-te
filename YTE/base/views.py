from django.db.models import Q
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *


# Create your views here.


def homePage(request):
    products = Product.objects.all()[:5]
    products_latest = Product.objects.all().order_by('-createAt')[:5]
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
    subTotal = 0
    try:
        order = Order.objects.get(user= user,isConfirmed = False)
        orderItem_set = order.orderitem_set.all()
    except Order.DoesNotExist:
        order = None
        orderItem_set = 0
        subTotal = 0.0
    if orderItem_set != 0:
        if order.orderitem_set.all().count() ==0:
            subTotal= 0.0
        elif order.orderitem_set.all().count() <2:
            subTotal = orderItem_set[0].price * orderItem_set[0].count
        else:
            for item in orderItem_set:
                subTotal += item.price*item.count

    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete':
            id = request.POST.get('id')
            delete_orderItem = OrderItem.objects.get(id = id)
            delete_orderItem.delete()
            if orderItem_set.count() ==0:
                orderItem_set = 0
            return redirect('cart')
        else:
            id = request.POST.get('id')
            update_orderItem = OrderItem.objects.get(id = id)
            count = request.POST.get('count')
            update_orderItem.count = count
            update_orderItem.save()
            return redirect('cart')
    context = {
        'orderItem_set' : orderItem_set,
        'subTotal': subTotal,
    }

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
    products = Product.objects.all()
    products_latest = Product.objects.all().order_by('-createAt')[:5]
    context = {
        'products': products,
        'products_latest': products_latest
    }

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
        order, created = Order.objects.get_or_create(user=request.user,isConfirmed = False)
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


def paymentPage(request):
    user = request.user
    subTotal = 0
    order = Order.objects.get(Q(user=user) & Q(isConfirmed = False))
    orderItem_set = order.orderitem_set.all()
    shippingAddress,create = ShippingAddress.objects.get_or_create(order=order)
    if orderItem_set.count()<2:
        subTotal = orderItem_set[0].price * orderItem_set[0].count
    else:
        for item in orderItem_set:
                subTotal += item.price*item.count
    
    
    if request.method == 'POST':
        firstName = request.POST.get('firstname')
        lastName = request.POST.get('lastname')
        phoneNum = request.POST.get('phonenumber')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        payment = request.POST.get('paymentMethod')
        totalPrice = request.POST.get('sumTotal')
        if user.first_name != firstName or user.last_name != lastName or user.email!= email:    
            user.first_name = firstName
            user.last_name = lastName
            user.email = email
            user.save()
        shippingAddress.address = address
        shippingAddress.city = city
        shippingAddress.phoneNumber = phoneNum
        order.paymentMethod = payment
        order.totalPrice = totalPrice
        order.isConfirmed = True
        order.save()
        shippingAddress.save()
        return redirect('my-orders')
    context={
        'shipping':shippingAddress,
        'orderItem_set':orderItem_set,
        'order':order,
        'subTotal':subTotal,
    }
    return render(
        request,
        'base/thanhtoan.html',
        context
    )


def search(request):
    if request.method == 'GET':   
        q =  request.GET.get('q')     

        products= Product.objects.filter(name__contains=q)
    else:
        products =Product.objects.all()
    context = {
        'products': products,
        'q': q
    }
    return render(
        request,
        'base/products.html',
        context
    )

@login_required(login_url='/login')
def myOrdersPage(request):
    user = request.user
    orders = user.order_set.all().order_by('-createAt')
    
    context = {
        'orders': orders
    }
    return render(
        request,
        'base/my-orders.html',
        context
    )
