from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserInfo(AbstractUser):
    tel = models.CharField(max_length=32, null=True, blank=True)