from django.db import models
from django.contrib.auth.models import User

class Budget():
    TYPES = [('MONTH','monthly'),('QUART','quarterly'),('YEAR','yearly')]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField()
    type = models.CharField(max_length=5,choices=TYPES)