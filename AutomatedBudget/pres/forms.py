from unicodedata import category, name
from django import forms

class BudgetCreationForm(forms.Form):
    TYPES = [('MONTH','monthly'),('QUART','quarterly'),('YEAR','yearly')]
    type = forms.ChoiceField(choices=TYPES)
    income = forms.FloatField()

class ConditionCreationForm(forms.Form):
    name = forms.CharField(max_length=30)
    value = forms.CharField(max_length=10)
    isExtendable = forms.BooleanField()

class ExpenseCreationForm(forms.Form):
    sum = forms.FloatField()
    category = forms.CharField(max_length=50)