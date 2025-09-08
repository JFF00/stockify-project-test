from django.db import models


class Product(models.Model):
    id_product = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=256)
    stock = models.IntegerField(default=0)
    unit_price = models.FloatField(default=0.0)
    created_at = models.DateField()



