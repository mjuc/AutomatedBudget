from django.urls import path
from . import views

urlpatterns = [
    path('updateExpense/',views.ExpenseUpdateView.as_view(),name="updateExpense")
]