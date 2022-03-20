from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField()

class Expense(models.Model):
    sum = models.CommaSeparatedIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Budget(models.Model):
    TYPES = [('MONTH','monthly'),('QUART','quarterly'),('YEAR','yearly')]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField()
    type = models.CharField(max_length=5,choices=TYPES)
    expenses = models.ForeignKey(Expense, on_delete=models.CASCADE)
    income = models.CommaSeparatedIntegerField()