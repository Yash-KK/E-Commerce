from django.shortcuts import render

# Models
from .models import (
    Product
)
from Category.models import (
    Category
)
# Create your views here.
def store_page(request, c_slug=None):
    if c_slug:
        all_products = Product.objects.filter(category__category_slug=c_slug)
        product_count = all_products.count()
    else:    
        all_products = Product.objects.all()
        product_count = all_products.count()
    context = {
        'all_products': all_products,
        'product_count':product_count
    }
    return render(request, 'Store/store.html',context)

def product_detail(request,c_slug=None, p_slug=None):
    if c_slug and p_slug:
        product_detail = Product.objects.get(category__category_slug = c_slug, product_slug=p_slug)
    
    context = {
        'pd':product_detail
    }
        
    return render(request ,'Store/productDetail.html',context)
