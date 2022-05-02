from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.landing),
    path('history/', views.history, name="history"),
    path('current/', views.current, name="current"),
    path('create/', views.create),
    path('error/', views.error)
]