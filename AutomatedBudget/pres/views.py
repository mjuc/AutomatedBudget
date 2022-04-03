from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def history(request):
    return render(request,'budgets/historic.html')

@login_required
def current(request):
    return render(request,'budgets/current.html')

@login_required
def create(request):
    pass
