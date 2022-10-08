from django.urls import path

from .import views

urlpatterns = [
    path("", views.store_page, name='store-page'),
    path("search/", views.search_functionality, name='search'),
    path("submit-review/<int:product_id>", views.submit_review, name='submit-review'), 
    path("<slug:c_slug>/", views.store_page, name='product-by-category'),
    path("<slug:c_slug>/<slug:p_slug>/", views.product_detail, name='product-detail'),
]
