from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('menu/', views.menu, name="menu"),
    path('deposit/', views.deposit, name="deposit"),
    path('profile/', views.profile, name="profile"),
    path('about/', views.about, name="about"),
    path('login/', views.LoginUser.as_view(), name="login"),
    path('register/', views.RegisterUser.as_view(), name="register"),
    path('logout/', views.logout_user, name='logout'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
]