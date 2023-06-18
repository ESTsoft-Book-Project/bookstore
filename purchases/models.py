from django.db import models
from django.conf import settings
from products.models import Product

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    stripe_checkout_session_id = models.CharField(max_length=220, blank=True, null=True)
    stripe_price = models.IntegerField(default=0)