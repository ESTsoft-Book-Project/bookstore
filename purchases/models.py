from django.db import models
from django.conf import settings
import stripe
from products.models import Product

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_name = models.CharField(max_length=255)
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

    stripe_price = models.IntegerField(default=1)
    stripe_price_id = models.CharField(max_length=220, blank=True, null=True)
    stripe_product_id = models.CharField(max_length=220, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stripe_price = self.product.price

    def __str__(self):
        return self.product.name
    
    def save(self, *args, **kwargs):
        if self.product.name:
            stripe_product_r = stripe.Product.create(name=self.product.name)
            self.stripe_product_id = stripe_product_r.id

        if not self.stripe_price_id:
            stripe_price_obj = stripe.Price.create(
                    product = self.stripe_product_id,
                    unit_amount=self.stripe_price,
                    currency='KRW'
                )
            self.stripe_price_id = stripe_price_obj.id
        super().save(*args, **kwargs)