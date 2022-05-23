from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from pres import models

@login_required
class ExpenseUpdateView(APIView):
    def post(self, request):
        savings = models.Savings.objects.filter(owner=request.user)
        expense = models.Expense.objects.filter(id=request.data.exp_id)
        expense.spent_sum += request.data.expSpentSum
        savings.saved_sum -= request.data.expSpentSum
        expense.save()
        savings.save()