#DJANGO
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)

#MODELS
from .models import (
    Product,
    ReviewRating
)
from acc.models import Account
from Category.models import (
    Category 
)
from Orders.models import (
    OrderProduct
)

#FORMS
from .forms import RatingForm

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
    
    if request.user.is_authenticated:    
        order_product = OrderProduct.objects.filter(user=request.user, product=product_detail.id).exists()
    else:
        order_product = None    
    
    reviews = ReviewRating.objects.filter(product=product_detail.id)
    context = {
        'pd':product_detail,
        'op': order_product,
        
        'reviews':reviews
    }        
    return render(request ,'Store/productDetail.html',context)


def submit_review(request,product_id):
    product = Product.objects.get(id=product_id)
    current_user = request.user
    ip = request.META.get("REMOTE_ADDR")
    previous_url = request.META.get("HTTP_REFERER")
    obj = ReviewRating()
    
    try:
        # update the review
        if request.method == 'POST':
            previous_rating = ReviewRating.objects.get(user=current_user, product=product)
            form = RatingForm(request.POST,instance=previous_rating)
            if form.is_valid():
                form.save()
                return redirect(previous_url)  
    except:        
        print("Except wala")
        # create a review       
        if request.method == 'POST':
           if request.method == 'POST':
            form = RatingForm(request.POST)
        
            if form.is_valid():
                obj.rating = request.POST['rating']
                obj.review = request.POST['review']
                obj.subject = request.POST['subject']
                
                obj.ip = ip
                obj.user = current_user
                obj.product = product
                obj.save()  
                return redirect(previous_url)

    return HttpResponse("Reviewed")