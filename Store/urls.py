from django.urls import path

from .import views

urlpatterns = [
    path("", views.store_page, name='store-page'),    
    path("<slug:c_slug>/", views.store_page, name='product-by-category'),
    path("<slug:c_slug>/<slug:p_slug>/", views.product_detail, name='product-detail'),
]
