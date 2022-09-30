from django.shortcuts import redirect, render


# Models
from .models import (
    Cart,
    CartItems
)
from Store.models import (
    Product
)
# Create your views here.
def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    
    cart = Cart.objects.filter(cart_id=_cart_id(request)).exists()
    if cart:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    else:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
    cart_item = CartItems.objects.filter(cart=cart, product=product).exists()
    if cart_item:
        cart_item = CartItems.objects.get(cart=cart, product=product)
        cart_item.quantity +=1
    else:
        cart_item = CartItems.objects.create(
            cart=cart,
            product=product,
            quantity = 1
        )     
    cart_item.save()
    
    return redirect('cart-page')

def cart_page(request,cart_items= None):
    total = 0
    tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id= _cart_id(request))
        cart_items = CartItems.objects.filter(cart=cart)       
        for item in cart_items:
            total += item.product.product_price * item.quantity
        tax = (total*2)/100
        grand_total = total + tax
    except Cart.DoesNotExist:
        pass    
    
    context = {
        'cart_items':cart_items,

        'total': total,
        'grand_total': grand_total,
        'tax': tax
    }
    return render(request, 'Cart/cart.html',context)


def decrement_item(request, id):
    product = Product.objects.get(id=id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItems.objects.get(cart=cart, product=product)
    print(cart_item)
    print(f"------>>>{product}")    
    if cart_item.quantity == 1:
        cart_item.delete()
    else:
        cart_item.quantity -=1
        cart_item.save()        
    return redirect('cart-page')

def remove_item(request,id):
    product = Product.objects.get(id=id)
    cart = Cart.objects.get(cart_id = _cart_id(request))
    cart_item = CartItems.objects.get(cart=cart, product=product)
    
    cart_item.delete()
    return redirect('cart-page') 
       