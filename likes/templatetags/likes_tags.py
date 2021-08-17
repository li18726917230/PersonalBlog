"""
模板标签文件
"""
from django import template
from ..models import LikeRecord,LikeCount
from user.models import User
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.simple_tag
def get_like_status(obj, user):
    content_type = ContentType.objects.get_for_model(obj)
    if user is '':
        return ''
    user = User.objects.get(name=user)
    if LikeRecord.objects.filter(content_type=content_type, object_id=obj.id, user=user).exists():
        return 'active'
    else:
        return ''
@register.simple_tag
def get_like_num(obj):
    content_type = ContentType.objects.get_for_model(obj)
    like_count, create = LikeCount.objects.get_or_create(content_type=content_type, object_id=obj.id)
    return like_count.liked_num
