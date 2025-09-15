from django.db import models

# Create your models here.
class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    username = models.TextField()
    email = models.EmailField()
    role = models.TextField() # change later
    password = models.TextField() #change later


