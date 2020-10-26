from django.db import models
from datetime import datetime

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    salt = models.CharField(max_length=128)
    hashed_password = models.CharField(max_length=400)
    phone_number = models.BigIntegerField()
    user_type = models.IntegerField(default=1) # normal user : 1 | worker : 2
    
    def __str__(self):
        return f"{self.username}"


class Trolly(models.Model):
    trolley_id = models.AutoField(primary_key=True)
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    isOccupied = models.BooleanField(default=False)
    last_update = models.DateTimeField()

    def __str__(self):
        return f'id : {self.trolley_id}'


class Occupied_trollies(models.Model):
    occupied_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trolly = models.OneToOneField(Trolly, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # trolly = models.ForeignKey(Trolly, on_delete=models.CASCADE)

    def __str__(self):
        return f'id = {self.occupied_id}'


