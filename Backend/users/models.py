from django.db import models

# Create your models here.
class User(AbstractUser):
    role = models.CharField(max_length=50, default='user')
    #user_id = models.AutoField(primary_key=True)
    ##username = models.TextField()
    email = models.EmailField()
    #role = models.TextField() # change later
    password = models.TextField() #change later


