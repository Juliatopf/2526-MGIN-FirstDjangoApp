from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Patient(User):
    birthday = models.DateTimeField()
    svnr = models.CharField(max_length=11)
