from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"), name="redirect-admin"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('userlogin', views.login_user, name="login-user"),
    path('user-register', views.registerUser, name="register-user"),
    path('logout', views.logoutuser, name='logout'),
    path('profile', views.profile, name='profile'),
    path('update-profile', views.update_profile, name='update-profile'),
    path('update-password', views.update_password, name='update-password'),
    path('', views.home, name='home-page'),

    # Box Type Management
    path('box-type', views.box_type_mgt, name='box-type-page'),
    path('manage-box-type', views.manage_box_type, name='manage-box-type'),
    path('save-box-type', views.save_box_type, name='save-box-type'),
    path('manage-box-type/<int:pk>', views.manage_box_type, name='manage-box-type-pk'),
    path('delete-box-type', views.delete_box_type, name='delete-box-type'),

    # Box Management
    path('box', views.box_mgt, name='box-page'),
    path('manage-box', views.manage_box, name='manage-box'),
    path('save-box', views.save_box, name='save-box'),
    path('manage-box/<int:pk>', views.manage_box, name='manage-box-pk'),
    path('delete-box', views.delete_box, name='delete-box'),

    # Inventory Management
    path('inventory', views.inventory, name='inventory-page'),
    path('inventory-history-page', views.inv_history, name='inventory-history-page'),
    path('stock/<int:pid>', views.manage_stock, name='manage-stock'),
    path('stock/<int:pid>/<int:pk>', views.manage_stock, name='manage-stock-pk'),
    path('save-stock', views.save_stock, name='save-stock'),
    path('delete-stock', views.delete_stock, name='delete-stock'),

    # Sales Management
    path('sales', views.sales_mgt, name='sales-page'),
    path('get-box', views.get_box, name='get-box'),
    path('save-sales', views.save_sales, name="save-sales"),
    path('export-sales/', views.export_sales, name='export-sales'),

    # Invoice Management
    path('invoices', views.invoices, name='invoice-page'),
    path('delete-invoice', views.delete_invoice, name='delete-invoice'),
]
