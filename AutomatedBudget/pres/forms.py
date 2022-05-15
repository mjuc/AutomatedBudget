from django import forms
from .models import Budget, Condition, Expense

class ConditionCreationForm(forms.ModelForm):
    class Meta:
        model = Condition
        fields = '__all__'

class ExpenseCreationForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'

class BudgetCreationForm(forms.ModelForm):
    class Meta:
        model = Budget
        exclude = ['owner','creation_date','annotation', 'expenses', 'conditions']

ExpenseFormset = forms.formset_factory(ExpenseCreationForm)
ConditionFormset = forms.formset_factory(ConditionCreationForm)