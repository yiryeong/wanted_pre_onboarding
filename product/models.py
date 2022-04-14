from django.db import models
from django.contrib.auth.models import User


class TotalFundingManager(models.Manager):
    def get_queryset(self):
        return super().annotate(total_funding=super().fundings.all().count())


class Product(models.Model):
    u = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    target_amount = models.IntegerField()
    one_time_funding = models.IntegerField()
    # objects = TotalFundingManager()
    end_date = models.DateTimeField()
    create_date = models.DateTimeField(auto_now_add=True)

