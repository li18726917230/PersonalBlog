"""
模板标签文件
"""
from django import template
from ..models import User

register = template.Library()
@register.simple_tag
def get_user(name):
    try:
        user = User.objects.get(name=name)
    except:
        user=''
    return user

