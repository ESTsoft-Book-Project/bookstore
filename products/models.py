from django.conf import settings
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, unique=False)
    handle = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # purchases


    def __str__(self):
        return self.name
