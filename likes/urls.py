from django.urls import path
from . import  views

urlpatterns = [
    path('',views.like,name='likes')
]