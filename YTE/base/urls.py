from django.urls import path
from . import views



urlpatterns = [
    path('',views.homePage,name = 'home'),
    path('cart',views.cart,name='cart'),
    path('login/',views.loginPage,name='login'),
    path('signup',views.signupPage,name='signup'),
    path('logout',views.logoutUser,name='logout'),
    path('products',views.productsPage,name='products-page'),
    path("product-info/<int:pk>", views.productInfo, name="product-info")
]