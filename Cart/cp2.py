from .views import _cart_id
from .models import (
    Cart,
    CartItems
)
 
def cart_count(request):
    count = 0
    try:
        if request.user.is_authenticated:
            cart_item = CartItems.objects.filter(user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItems.objects.filter(cart=cart)[:]
        for item in cart_item:
            count += item.quantity
    except Cart.DoesNotExist:
        pass        
    
    return {
        'cart_count':count
    }
    