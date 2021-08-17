"""
模板标签文件
"""
from django import template
from ..models import BlogType

register = template.Library()
@register.simple_tag
def get_blogtype():
    blog_type = BlogType.objects.all()
    return blog_type

