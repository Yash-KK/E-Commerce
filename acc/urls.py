from django.urls import path
from .import views

urlpatterns = [
    path("register/", views.register_page, name='register-page'),
    path("login/", views.login_page, name='login-page'),
    path("logout/", views.logout_page, name='logout-page'),
    
    path("dashboard/", views.dashboard, name='dashboard'),
    path("my-orders/", views.my_orders, name='my-orders'),
    path("edit-profile/", views.edit_profile, name='edit-profile'),
    path("change-password/", views.change_password, name='change-password'),
    path("order-detail/<int:order_id>", views.order_detail, name='order-detail'),
    
    path("activate/<uidb64>/<token>/", views.activate, name='activate')
]
