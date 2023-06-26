from django.db import models
from django.conf import settings
from products.models import Product
import stripe
class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product)
    timestamp = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    stripe_checkout_session_id = models.CharField(max_length=220, blank=True, null=True)
    stripe_price = models.IntegerField(default=0)

    kakaopay_checkout_tid = models.CharField(max_length=20, blank=True, null=True)
    kakaopay_price = models.IntegerField(default=0)
