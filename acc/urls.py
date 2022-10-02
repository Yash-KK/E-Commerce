from django.urls import path
from .import views

urlpatterns = [
    path("register/", views.register_page, name='register-page'),
    path("login/", views.login_page, name='login-page'),
    path("logout/", views.logout_page, name='logout-page'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("activate/<uidb64>/<token>/", views.activate, name='activate')
]
