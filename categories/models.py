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