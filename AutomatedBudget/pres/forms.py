from django import forms

class BudgetCreationForm(forms.Form):
    TYPES = [('MONTH','monthly'),('QUART','quarterly'),('YEAR','yearly')]
    type = forms.ChoiceField(choices=TYPES)