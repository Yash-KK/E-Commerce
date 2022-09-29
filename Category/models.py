from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    category_image = models.ImageField(upload_to='Images/')
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def category_url(self):
        return reverse('product-by-category', args=[self.category_slug])    
    def __str__(self):
        return f"{self.category_name}" 