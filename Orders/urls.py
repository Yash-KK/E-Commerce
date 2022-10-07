from django.urls import path

from .import views

urlpatterns = [
    path("", views.place_order, name='place-order'),
    path("make-payment/", views.make_payment, name='payments'),
    path("order_complete/", views.order_complete, name='order_complete')
]
