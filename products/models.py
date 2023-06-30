from django.conf import settings
from django.db import models
import stripe
from django.urls import reverse

from users.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    handle = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=0)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    stock = models.IntegerField(default=0)
    
    def get_absolute_url(self):
        return reverse("book:book_detail", kwargs={"handle": self.handle})
    
    def get_image_url(self):
        if self.image:
            return self.image.url
        return ''

#Comment
class Comment(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment