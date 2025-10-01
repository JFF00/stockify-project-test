from django.db import models

# Create your models here.
class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'categorys'
        verbose_name_plural = 'Categories'

class Product(models.Model):
    id_product = models.AutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    stock = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)  # ✅ fecha automática
    # Opción A: permitir nulo (no obligamos a elegir)
    id_category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )


class Movement(models.Model):
    id_movement = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    date = models.DateField()
    type = models.TextField() # change later 
    records = models.ManyToManyField(Product, through='Record')


class Record(models.Model):
    id_movement = models.ForeignKey(Movement, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.FloatField()
