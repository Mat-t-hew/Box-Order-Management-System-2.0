from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('profile/', views.profile, name='profile'),
    path('update-password/', views.update_password, name='update-password'),
    path('register/', views.register, name='register-user'),
    path('box-types/', views.box_types, name='category-list'),
    path('inventory/', views.inventory, name='inventory-list'),
    path('sales/', views.sales_transactions, name='sales-list'),
    path('share-file/', views.share_file, name='share-file'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]
