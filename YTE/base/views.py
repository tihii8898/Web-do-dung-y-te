from email import message
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.


def homePage(request):
    products = Product.objects.all()
    context = {
        'products': products
    }

    return render(
        request,
        'base/home.html',
        context
    )

@login_required(login_url='/login')
def cart(request):
    user = request.user
    

    context = {}

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