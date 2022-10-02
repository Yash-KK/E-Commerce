from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)
# Models
from .models import (
    Product
)
from Category.models import (
    Category 
)
# Create your views here.

def search_functionality(request):
    all_products = None
    product_count = 0
    if request.method == 'GET':
        key = request.GET['keyword']
        if key:
            all_products = Product.objects.filter(
                Q(product_name__icontains=key) | Q(description__icontains=key)
            )
            product_count = all_products.count()
    
    context = {
        'all_products': all_products,
        'product_count': product_count
    }     
    
    return render(request, 'Store/store.html', context)
   

def store_page(request, c_slug=None):   
    if c_slug:
        all_products = Product.objects.filter(category__category_slug=c_slug)
        product_count = all_products.count()
        
        page = request.GET.get('page',1)
        paginator = Paginator(all_products,6)   
        try:
            pp = paginator.page(page)
        except PageNotAnInteger:
            pp = paginator.page(1)
        except EmptyPage:
            pp = paginator.page(paginator.num_pages)               
    else:    
        all_products = Product.objects.all()
        product_count = all_products.count()
        
         
        page = request.GET.get('page',1)
        paginator = Paginator(all_products,6)
        try:
            pp = paginator.page(page)
        except PageNotAnInteger:
            pp = paginator.page(1)
        except EmptyPage:
            pp = paginator.page(paginator.num_pages)   
            
    context = {       
        'all_products':pp,
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
