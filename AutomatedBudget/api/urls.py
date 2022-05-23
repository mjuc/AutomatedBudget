from django.urls import path
from . import views

urlpatterns = [
    path('updateExpense/',views.ExpenseUpdateView)
]