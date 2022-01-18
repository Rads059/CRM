from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

class User(AbstractUser):
    pass

class Agent(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Lead(models.Model):
    fname=models.CharField(max_length=16)
    lname=models.CharField(max_length=16)
    email=models.EmailField(max_length=32)
    PHONE_VALID = RegexValidator(r'^([0-9]){10}', "Phone number invalid.")
    phone = models.CharField(max_length=10, validators=[PHONE_VALID])
    SOURCE_CHOICES =   (
        ('BCA','BCA'),
        ('MCA', 'MCA'),
        ('BTECH-CS','BTECH-CS'),
        ('BTECH-ECE','BTECH-ECE')
    )
    course=models.CharField(choices=SOURCE_CHOICES, max_length=64)
    claimed=models.ForeignKey(Agent,on_delete=models.SET_NULL,
    null=True, blank=True)
    def __str__(self):
        return self.fname+" "+self.lname




