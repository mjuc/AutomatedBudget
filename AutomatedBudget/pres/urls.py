from django.urls import path
from . import views 
    
urlpatterns = [
        path('', views.index),
        path('login/', views.signin),
        path('logout/', views.signout),
        path('signup/', views.signup),
]