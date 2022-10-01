from email.policy import default
from django.db import models
from django.urls import reverse

# Models
from Category.models import (
    Category 
)
# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=150)
    product_slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField()
    product_price = models.FloatField()
    product_image = models.ImageField(upload_to = 'Images/Products/')
    
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    
    
    
    def product_url(self):
        return reverse('product-detail', args =[self.category.category_slug, self.product_slug])
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    
    def __str__(self):
        return f"{self.product_name}"


VAR_CATEGORY_CHOICES = (
    ("Color", "Color"),
    ("Size", "Size"),
   
)
class VariationManager(models.Manager):
    def colors(self):
        return self.filter(variation_category='Color')
    
    def sizes(self):
        return self.filter(variation_category='Size')

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=VAR_CATEGORY_CHOICES)
    variation_value = models.CharField(max_length=100)   
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    objects = VariationManager()
    def __str__(self):
        return f"{self.product}: Variation({self.variation_value})" 
         