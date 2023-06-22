from django.db import models
from django.conf import settings
from products.models import Product


class Cart(models.Model):
    product = models.ForeignKey(Product, to_field="handle", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    checked = models.BooleanField(default=False)