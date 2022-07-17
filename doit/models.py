from django.db import models

from core.models import TimeStampModel

class User(TimeStampModel):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=100)
    etc_info = models.CharField(max_length=500, null=True)

    class Meta:
        abstract = True
        db_table = 'users'