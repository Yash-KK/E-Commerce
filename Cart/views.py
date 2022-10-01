from django.http import HttpResponse
from django.shortcuts import redirect, render


# Models
from .models import (
    Cart,
    CartItems
)
from Store.models import (
    Product,
    Variation
)
# Create your views here.
def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_ke_variations = []
    if request.method == 'POST':       
        for item in request.POST:
            key = item
            value = request.POST[key]                
            try:
                # variations = Variation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact=value)
                variations = Variation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact=value)
                product_ke_variations.append(variations)    
            except:
                print("Nahi HUa")
                pass     
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
        cart_item = CartItems.objects.filter(cart=cart, product=product)
        
        exist_var = []
        item_id = []
        for item in cart_item:            
            x = item.variations.all()
            exist_var.append(list(x))
            item_id.append(item.id)
       # CONTINUE FROM HERE-----------------------> IF THE PRODUCT VARIATIONS EXIST IN EXISTING VARIATIONS ,,,,,,
        
        if product_ke_variations in exist_var:
           # Increase the item quantity
           index = exist_var.index(product_ke_variations)
           id = item_id[index]           
           item = CartItems.objects.get(product=product, id=id)
           item.quantity +=1
           item.save()
           
        else:
            item = CartItems.objects.create(product=product, cart=cart, quantity=1)
            
            if len(product_ke_variations)>0:
                item.variations.clear()
                item.variations.add(*product_ke_variations)
            item.save()
    else:
        item = CartItems.objects.create(
            cart=cart,
            product=product,
            quantity = 1
        ) 
        if len(product_ke_variations)> 0:
            item.variations.clear()
            item.variations.add(*product_ke_variations)              
        item.save()    
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


def decrement_item(request, id,cart_item_id):
    product = Product.objects.get(id=id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    try:
        cart_item = CartItems.objects.get(cart=cart, product=product,id=cart_item_id)
        print(cart_item)
        print(f"------>>>{product}")    
        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -=1
            cart_item.save()      
    except:
        pass          
    return redirect('cart-page')

def remove_item(request,id,cart_item_id):
    product = Product.objects.get(id=id)
    cart = Cart.objects.get(cart_id = _cart_id(request))
    try:
        cart_item = CartItems.objects.get(cart=cart, product=product,id=cart_item_id)    
        cart_item.delete()
    except:
        pass    
    return redirect('cart-page') 
       