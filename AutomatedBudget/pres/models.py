from re import A
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)

class Expense(models.Model):
    sum = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Condition(models.Model):
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=10)
    isExtendable = models.BooleanField()

class Budget(models.Model):
    TYPES = [('MONTH','monthly'),('QUART','quarterly'),('YEAR','yearly')]
    ANNOTATIONS = [('LOSS','loss'),('EVEN','even'),('NORMAL','')]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField()
    type = models.CharField(max_length=5,choices=TYPES)
    expenses = models.ForeignKey(Expense, on_delete=models.CASCADE)
    income = models.FloatField()
    annotation = models.CharField(max_length=4,choices=ANNOTATIONS)