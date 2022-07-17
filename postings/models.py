from pydoc import classify_class_attrs
from unittest.util import _MAX_LENGTH
from django.db import models

from django.contrib.auth.models import User
from core.models import TimeStampModel

class Post(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(max_length=200)

    class Meta:
        db_table = 'postings'