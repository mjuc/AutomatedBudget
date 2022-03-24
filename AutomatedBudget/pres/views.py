from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def history(request):
    pass

@login_required
def current(request):
    pass

@login_required
def create(request):
    pass
