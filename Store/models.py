from email.policy import default
from django.db import models
from django.urls import reverse

# Models
from Category.models import (
    Category 
)
from acc.models import (
    Account
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
    
    def avg_review(self):
        avg = 0
        count = 0
        review_ratings = ReviewRating.objects.filter(product=self)
        for rev in review_ratings:
            avg += rev.rating
            count +=1
        try:    
            avg = avg/count   
        except ZeroDivisionError:
            avg = 0
                 
        if review_ratings != 0.0:            
            return round(float(avg),2)
        
        
        return float(avg)
    
    def total_reviews(self):       
        reviews = ReviewRating.objects.filter(product=self).count()
        return reviews
    
    
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

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    
    subject = models.CharField(max_length=50,blank=True)
    review = models.TextField(max_length=250,blank=True)    
    rating = models.FloatField()
    
    ip = models.CharField(max_length=250)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def __str__(self):
        return f"{self.user.first_name}: {self.rating}"
    
         