from django.db import models
from django.conf import settings

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    