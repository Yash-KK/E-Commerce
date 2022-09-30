from django.urls import path

from .import views
urlpatterns = [
    path("", views.cart_page, name='cart-page'),
    path("decrement/<int:id>/", views.decrement_item, name='decrement-item'),
    path("remove/<int:id>/", views.remove_item, name='remove-item'),
    path("<int:product_id>/", views.add_to_cart, name='add-to-cart'),
    
]
