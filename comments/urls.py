from django.urls import path
from . import  views

urlpatterns = [
    path('',views.comments,name='comments'),
    path('reply/',views.reply,name='reply')
]