from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import BudgetCreationForm, ConditionFormset, ExpenseFormset

def landing(request):
    return render(request,'budgets/landing_page.html')

@login_required
def history(request):
    return render(request,'budgets/historic.html')

@login_required
def current(request):
    return render(request,'budgets/current.html')

@login_required
def create(request):
    if request.method == 'POST':
        form = BudgetCreationForm(request.POST)
        expenseFormset = ExpenseFormset(request.POST)   
        conditionFormset = ConditionFormset(request.POST)
        if form.is_valid() and expenseFormset.is_valid() and conditionFormset.is_valid():
            conditions = []
            budget = form.save(commit=False)
            for expForm in expenseFormset:
                expense = expForm.save(commit=False)
                budget.expenses += expense
                expense.save()
            for condForm in conditionFormset:
                condition = condForm.save(commit=False)
                conditions.append(condition)
            #call genetic algo here
            budget.save()
    elif request.method == 'GET':
        form = BudgetCreationForm()
        expenseFormset = ExpenseFormset()   
        conditionFormset = ConditionFormset()

        return render(request, 'budgets/create.html', {'form': form, 
        'expenseFormset': expenseFormset,
        'conditionFormset': conditionFormset })
