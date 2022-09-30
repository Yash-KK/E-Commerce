from django.shortcuts import render

# Model
from Store.models import (
    Product
)
# Create your views here

def home(request):
    all_products = Product.objects.all()
    context = {
        'all_products': all_products
    }
    return render(request, 'home.html',context)


