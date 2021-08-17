from django.urls import path
from . import  views
urlpatterns = [
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('code_send/',views.code_send,name='code_send'),
    path('code_val/',views.code_val,name='code_val'),
    path('user_val/',views.user_val,name='user_val'),
    path('login_phone_val/',views.login_phone_val,name='login_phone_val'),
    path('user_alter/',views.user_alter,name='user_alter'),
    path('pwd_alter/',views.pwd_alter,name='pwd_alter'),
    path('user_adder/',views.user_adder,name='user_adder'),
]