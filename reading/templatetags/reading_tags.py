"""
模板标签文件
"""
from django import template
from ..models import Read
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.simple_tag
def get_read_num(obj):
    content_type = ContentType.objects.get_for_model(obj)
    read, create = Read.objects.get_or_create(content_type=content_type, object_id=obj.id)
    return read.read_num
