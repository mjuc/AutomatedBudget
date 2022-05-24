from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from pres import models

class ExpenseUpdateView(APIView):
    def post(self, request):
        user = User.objects.get(id=request.data["user_id"])
        savings = models.Savings.objects.get(owner=user)
        expense = models.Expense.objects.get(id=request.data["exp_id"])
        if request.data["expSpentSum"] != '':
            expense.spent_sum += float(request.data["expSpentSum"])
            savings.saved_sum -= float(request.data["expSpentSum"])
            expense.save()
            savings.save()
            return JsonResponse({"Effect": True})
        else:
            return JsonResponse({"Effect": False})