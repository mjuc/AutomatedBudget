from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    sum = models.FloatField()
    category = models.CharField(max_length=50)

class Condition(models.Model):
    name = models.CharField(max_length=30)
    isExtendable = models.BooleanField(blank=False)
    value = models.CharField(max_length=10)

class Budget(models.Model):
    TYPES = [('MONTH','monthly'),('QUART','quarterly'),('YEAR','yearly')]
    ANNOTATIONS = [('LOSS','loss'),('EVEN','even'),('NORMAL','')]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField()
    type = models.CharField(max_length=5,choices=TYPES)
    expenses = models.ManyToManyField(Expense)
    conditions = models.ManyToManyField(Condition)
    income = models.FloatField()
    annotation = models.CharField(max_length=4,choices=ANNOTATIONS)