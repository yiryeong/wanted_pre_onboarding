from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class Funding(models.Model):
    u = models.ForeignKey(User, on_delete=models.CASCADE)
    p = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    funding_date = models.DateTimeField(auto_now_add=True)
