from django.db import models

# Create your models here.
class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    created_at = models.DateField()

    class Meta:
        db_table = 'categorys'
        verbose_name_plural = 'Categories'

class Product(models.Model):
    id_product = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=256)
    stock = models.IntegerField(default=0)
    unit_price = models.FloatField(default=0.0)
    created_at = models.DateField()


class Movement(models.Model):
    id_movement = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    date = models.DateField()
    type = models.TextField() # change later 
    records = models.ManyToManyField(Product, through='Record')


class Record(models.Model):
    id_movement = models.ForeignKey(Movement, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.FloatField()
