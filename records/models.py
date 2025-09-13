from django.db import models

# Create your models here.
class Record(models.Model):
    pk = models.CompositePrimaryKey("id_movement", "id_product")
    id_movement = models.ForeignKey('movements.Movement', on_delete=models.CASCADE)
    id_product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    amount = models.FloatField()