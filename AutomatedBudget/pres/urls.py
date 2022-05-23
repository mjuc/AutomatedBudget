from django.urls import path
from . import views

urlpatterns = [
    path('',views.landing),
    path('history/', views.history, name="history"),
    path('current/', views.current, name="current"),
    path('create/', views.create, name="create"),
    path('error/', views.error)]