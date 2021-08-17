from django.shortcuts import render


def home(request):
    response =render(request, 'home.html')
    # 清除cookie
    response.delete_cookie('page')
    return response
