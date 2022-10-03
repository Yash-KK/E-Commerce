from django.db import models

# Models
from Category.models import (
    Category
)
from Store.models import (
    Product,
    Variation
)
from acc.models import (
    Account
)
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add= True)
    
    def __str__(self):
        return f"{self.cart_id}"
    
class CartItems(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    variations = models.ManyToManyField(Variation,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.product.product_price * self.quantity
    
    def __str__(self):
        return f"{self.product}. Quantity: {self.quantity}"
        