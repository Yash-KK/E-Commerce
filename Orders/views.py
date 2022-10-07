from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

import json
import razorpay
from greatKart.settings import (
    RAZORPAY_API_KEY_ID,
    RAZORPAY_API_KEY_SECRET
)

#PYTHON
import datetime

#MODELS
from Store.models import (
    Product
)
from Cart.models import (
    Cart,
    CartItems
)
from .models import (
    Order,
    Payment ,
    OrderProduct
)
#FORMS
from .forms import OrderForm


client = razorpay.Client(auth=(RAZORPAY_API_KEY_ID, RAZORPAY_API_KEY_SECRET))
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
            
            # order creatiion of razorpay
            DATA = {
                "amount": grand_total*100,
                "currency": "INR",
                "payment_capture": 1,
            }
            payment_order = client.order.create(data=DATA)
            print(f"Payment Order: {payment_order}")
            
            payment_order_id = payment_order['id']
            context = {
                'order':order,
                'total':total,
                'tax': tax,
                'grand_total':grand_total,                
                'cart_items':cart_items,     
                
                'api_key_id': RAZORPAY_API_KEY_ID,
                'order_id': payment_order_id,          
            }
            return render(request, 'Orders/make_payment.html', context)
        else:
            print(form.errors)
            return HttpResponse("Error")            
    else:
        return redirect('checkout')
    
    
def make_payment(request):
    print("did it enter this function?")
    body = json.loads(request.body)
    print(body)
    
    order_num = body['orderID']
    # Fetching the Order instance because we need order_total
    order = Order.objects.get(user=request.user, order_number=order_num)
    total_amount = order.order_total
    
    payment = Payment.objects.create(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        status = body['status'],
        amount_paid = total_amount
    )    
    order.payment = payment
    order.is_ordered = True    
    order.save()
    payment.save()
    
    cart_items = CartItems.objects.filter(user=request.user)
    for item in cart_items:
        order_product = OrderProduct()
        order_product.order_id = order.id
        order_product.payment = payment
        order_product.user = request.user
        order_product.product_id = item.product_id
        order_product.quantity = item.quantity
        order_product.product_price = item.product.product_price
        order_product.ordered = True
        order_product.save()
        
        
        # adding the variations of the item to the order_product
        cart_item = CartItems.objects.get(id=item.id)
        product_variations = cart_item.variations.all()
        order_product.variations.set(product_variations)
        order_product.save()
       
        # reduce the quantity of the product(stock) from the Product model
        product = Product.objects.get(id=item.product.id)
        product.stock -= item.quantity
        product.save()
        print("reduced the quantity")
    
    # delete the cart Item    
    cart_item_to_delete = CartItems.objects.filter(user=request.user)
    cart_item_to_delete.delete()
        
    # sending order_number and transaction id to JS
      
    data = {
        'order_number': order.order_number,
        'transID':payment.payment_id
    }
    return JsonResponse(data)
    
def order_complete(request):
    order_number = request.GET['order_number']
    transID = request.GET['payment_id']
    
    try:
        
        order = Order.objects.get(order_number=order_number)
        order_products = OrderProduct.objects.filter(order=order)
        
        sub_total = 0
        for item in order_products:
            sub_total += item.product_price * item.quantity
            
        payment = Payment.objects.get(payment_id = transID)
        context = {
            'order': order,
            'order_products':order_products,
            'payment': payment,
            'sub_total': sub_total
        }
        return render(request, 'Orders/order_complete.html',context)

    except Order.DoesNotExist or Payment.DoesNotExist:
        return redirect('home')
   
  