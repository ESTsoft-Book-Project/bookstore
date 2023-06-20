from django.conf import settings
from django.db import models
import stripe
from django.urls import reverse

class Product(models.Model):
    name = models.CharField(max_length=255, unique=False)
    handle = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # purchases
    stripe_price = models.IntegerField(default=999) # 100 * price
    stripe_price_id = models.CharField(max_length=220, blank=True, null=True)
    stripe_product_id = models.CharField(max_length=220, blank=True, null=True)


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.name:
            stripe_product_r = stripe.Product.create(name=self.name)
            self.stripe_product_id = stripe_product_r.id
        
        if not self.stripe_price_id:
            stripe_price_obj = stripe.Price.create(
                    product = self.stripe_product_id,
                    unit_amount=self.stripe_price,
                    currency="usd",
                )
            self.stripe_price_id = stripe_price_obj.id
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("book:book_detail", kwargs={"handle": self.handle})