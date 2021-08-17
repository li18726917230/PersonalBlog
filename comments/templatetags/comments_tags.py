"""
模板标签文件
"""
from django import template
from ..models import Comments


register = template.Library()
@register.simple_tag
def get_comments(id):
    comments = Comments.objects.filter(object_id=id,replycomment=None)
    return comments

