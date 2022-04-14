from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce


class TotalFundingManager(models.Manager):
    def get_total_funding(self):
        return self.annotate(total_funding=Coalesce(Sum("funding__price"), 0))


class Product(models.Model):
    u = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    target_amount = models.IntegerField()
    one_time_funding = models.IntegerField()
    objects = TotalFundingManager()
    end_date = models.DateTimeField()
    create_date = models.DateTimeField(auto_now_add=True)
