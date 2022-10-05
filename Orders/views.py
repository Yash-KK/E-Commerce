from django.http import HttpResponse
from django.shortcuts import redirect, render

#PYTHON
import datetime
#MODELS
from Cart.models import (
    Cart,
    CartItems
)
from .models import (
    Order
)
#FORMS
from .forms import OrderForm
# Create your views here.
def place_order(request):
    current_user = request.user
    cart_items = CartItems.objects.filter(user=current_user)
    
    total = 0
    tax = 0
    grand_total = 0
    quantity = 0
    for item in cart_items:
        total += item.product.product_price * item.quantity
    tax = (2*total)/100
    grand_total = total + tax
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        # print(form)
        print(form.is_valid())
        if form.is_valid():
            data = Order()      
            data.user = current_user    
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']
            data.order_note = form.cleaned_data['order_note']
            print(f"{data.first_name}:{data.last_name}:{data.email}:{data.phone}:{data.address_line_1}:{data.address_line_2}:{data.city}:{data.state}:{data.country}")
            
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            current_date = datetime.datetime.now().strftime("%I:%M%p on %B-%d-%Y")
            data.order_number = str(data.id) + current_date
            print(data.order_number)
            data.save()
            
            order = Order.objects.get(user=current_user, order_number = data.order_number, is_ordered=False)
            
            context = {
                'order':order,
                'total':total,
                'tax': tax,
                'grand_total':grand_total,
                
                'cart_items':cart_items
            }
            return render(request, 'Orders/make_payment.html', context)
        else:
            print(form.errors)
            return HttpResponse("Error")            
    else:
        return redirect('checkout')
    
    
def make_payment(request):
    return render(request, 'Orders/make_payment.html')
    