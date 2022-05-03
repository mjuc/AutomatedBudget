from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import BudgetCreationForm, ConditionFormset, ExpenseFormset
from .budget_creation import budgetCreationGA
from .models import Budget, Expense

def landing(request):
    return render(request,'budgets/landing_page.html')

@login_required
def history(request):
    budgets = Budget.objects.all()
    return render(request,'budgets/historic.html',context={"budgets": budgets})

@login_required
def current(request):
    budget = Budget.objects.last()
    return render(request,'budgets/current.html',context={"budget": budget})

@login_required
def error(request):
    return render(request,'budgets/error.html')

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
                budget.expenses.add(expense)
                expense.save()
            for condForm in conditionFormset:
                condition = condForm.save(commit=False)
                conditions.append(condition)
            inLimit, newExpenses = budgetCreationGA(budget.income,budget.expenses,conditions)
            budget.annotation = newExpenses["annotation"]
            if inLimit:
                for exp in newExpenses["calculatedExpenses"]:
                    expense = Expense()
                    expense.category = exp["category"]
                    expense.sum = exp["sum"]
                    budget.expenses.add(expense)
                    expense.save()
            budget.owner = request.user
            budget.save()
            return redirect(current)
        else:
            return redirect(error)
    elif request.method == 'GET':
        form = BudgetCreationForm()
        expenseFormset = ExpenseFormset()   
        conditionFormset = ConditionFormset()

        return render(request, 'budgets/create.html', {'form': form, 
        'expenseFormset': expenseFormset,
        'conditionFormset': conditionFormset })
