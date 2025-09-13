from django.db import models

# Create your models here.
class Movement(models.Model):
    id_movement = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    date = models.DateField()
    type = models.TextField() # change later 