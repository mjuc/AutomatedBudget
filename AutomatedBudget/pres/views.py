from math import floor
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import BudgetCreationForm, ConditionFormset, ExpenseFormset
from .budget_creation import budgetCreationGA
from .models import Budget, Expense, Savings

def landing(request):
    return render(request,'budgets/landing_page.html')

@login_required
def history(request):
    budgets = Budget.objects.all()
    return render(request,'budgets/historic.html',context={"budgets": budgets})

@login_required
@ensure_csrf_cookie
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
        savings, instanceFound = Savings.objects.get_or_create(owner=request.user)
        if form.is_valid() and expenseFormset.is_valid() and conditionFormset.is_valid():
            conditions = []
            expenses = []
            budget = form.save(commit=False)
            savedSum = budget.income
            budget.owner = request.user
            budget.save()
            for expForm in expenseFormset:
                expense = expForm.save(commit=False)
                if expense.sum != None:
                    expenses.append(expense.sum)
                    expense.spent_sum = expense.sum
                    savedSum -= expense.sum
                    expense.save()
                    budget.expenses.add(expense)
            
            savings.saved_sum += savedSum
            savings.save()

            for condForm in conditionFormset:
                tmp = {}
                condition = condForm.save(commit=False)
                if condition.name != None:
                    tmp["name"] = condition.name
                    tmp["value"] = condition.value
                    tmp["isExtendable"] = condition.isExtendable
                    conditions.append(tmp)
            inLimit, newExpenses = budgetCreationGA(budget.income,expenses,conditions,savings.saved_sum)
            budget.annotation = newExpenses["annotation"]
            if inLimit:
                for exp in newExpenses["calculatedExpenses"]:
                    expense = Expense()
                    expense.category = exp["category"]
                    expense.sum = floor(exp["sum"])
                    expense.spent_sum = 0
                    expense.save()
                    budget.expenses.add(expense)
                    
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
