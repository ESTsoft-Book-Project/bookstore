from django.db import models
from django.conf import settings
from products.models import Product

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product)
    timestamp = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    provider = models.CharField(max_length=220, blank=True, null=True)

    stripe_checkout_session_id = models.CharField(max_length=220, blank=True, null=True)
    stripe_price = models.IntegerField(default=0)

    kakaopay_checkout_tid = models.CharField(max_length=20, blank=True, null=True)
    kakaopay_price = models.IntegerField(default=0)

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)