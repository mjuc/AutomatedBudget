from django.urls import path, include
from . import views

urlpatterns = [
    path('history/', views.history, name="history"),
    path('current/', views.current, name="current"),
    path('upload/', views.upload)
]